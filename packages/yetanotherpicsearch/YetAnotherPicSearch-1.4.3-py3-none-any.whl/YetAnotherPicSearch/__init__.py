import re
from typing import Any, Dict, List, Optional, Tuple, Union

import arrow
from nonebot.adapters.onebot.v11 import (
    ActionFailed,
    Bot,
    GroupMessageEvent,
    Message,
    MessageEvent,
    PrivateMessageEvent,
)
from nonebot.matcher import Matcher
from nonebot.params import CommandArg
from nonebot.plugin.on import on_command, on_message
from nonebot.rule import Rule
from tinydb import JSONStorage, Query, TinyDB
from tinydb.middlewares import CachingMiddleware

from .ascii2d import ascii2d_search
from .cache import clear_expired_cache, exist_in_cache
from .config import config
from .ehentai import ehentai_search
from .result import Result
from .saucenao import saucenao_search


async def _to_me(bot: Bot, event: MessageEvent) -> bool:
    msgs = event.message
    at_me = bool([i for i in msgs if i.type == "at" and i.data["qq"] == bot.self_id])
    if event.reply:
        has_image = bool([i for i in event.reply.message if i.type == "image"])
    else:
        has_image = bool([i for i in msgs if i.type == "image"])
    if isinstance(event, PrivateMessageEvent):
        return has_image and event.to_me and config.search_immediately
    return has_image and (event.to_me or at_me)


IMAGE_SEARCH = on_message(rule=Rule(_to_me), priority=5)
IMAGE_SEARCH_MODE = on_command("搜图", priority=5)


@IMAGE_SEARCH_MODE.handle()
async def handle_first_receive(matcher: Matcher, args: Message = CommandArg()) -> None:
    mode, purge = get_args(args)
    matcher.state["ARGS"] = (mode, purge)
    if [i for i in args if i.type == "image"]:
        matcher.set_arg("IMAGES", args)


async def image_search(
    url: str,
    mode: str,
    purge: bool,
    proxy: Optional[str],
    hide_img: bool = config.hide_img,
) -> Union[List[str], Any]:
    db = TinyDB(
        "cache.json",
        storage=CachingMiddleware(JSONStorage),  # type: ignore
        encoding="utf-8",
        sort_keys=True,
        indent=4,
        ensure_ascii=False,
    )
    image_md5 = re.search("[A-F0-9]{32}", url)[0]  # type: ignore
    _result = exist_in_cache(db, image_md5, mode)
    cached = bool(_result)
    if purge or not _result:
        result_dict: Dict[str, Any] = {}
        if mode == "a2d":
            result_dict["ascii2d"] = await ascii2d_search(url, proxy, hide_img)
        elif mode == "ex":
            result_dict["ex"] = await ehentai_search(url, proxy, hide_img)
        else:
            result_dict["saucenao"] = await saucenao_search(url, mode, proxy, hide_img)
        result_dict["mode"] = mode
        result_dict["image_md5"] = image_md5
        result_dict["update_at"] = arrow.now().for_json()
        _result = Result(result_dict)
        db.upsert(
            _result.__dict__, (Query().image_md5 == image_md5) & (Query().mode == mode)
        )
    clear_expired_cache(db)
    db.close()
    if mode == "a2d":
        final_res = _result.ascii2d
    elif mode == "ex":
        final_res = _result.ex
    else:
        final_res = _result.saucenao
    if cached and not purge:
        return [f"[缓存] {i}" for i in final_res]
    return final_res


def get_image_urls(msg: Message) -> List[str]:
    return [i.data["url"] for i in msg if i.type == "image" and i.data.get("url")]


def get_args(msg: Message) -> Tuple[str, bool]:
    mode = "all"
    plain_text = msg.extract_plain_text()
    args = ["pixiv", "danbooru", "doujin", "anime", "a2d", "ex"]
    if plain_text:
        for i in args:
            if f"--{i}" in plain_text:
                mode = i
                break
    purge = "--purge" in plain_text
    return mode, purge


@IMAGE_SEARCH.handle()
@IMAGE_SEARCH_MODE.got("IMAGES", prompt="请发送图片")
async def handle_image_search(bot: Bot, event: MessageEvent, matcher: Matcher) -> None:
    message = event.reply.message if event.reply else event.message
    image_urls = get_image_urls(message)
    if not image_urls:
        await IMAGE_SEARCH_MODE.reject()
    if "ARGS" in matcher.state:
        mode, purge = matcher.state["ARGS"]
    else:
        mode, purge = get_args(event.message)
    for i in image_urls:
        msg_list = await image_search(i, mode, purge, config.proxy)
        if isinstance(event, PrivateMessageEvent):
            for msg in msg_list:
                await bot.send_private_msg(user_id=event.user_id, message=msg)
        elif isinstance(event, GroupMessageEvent):
            flag = config.group_forward_search_result and len(msg_list) > 1
            if flag:
                try:
                    await bot.send_group_forward_msg(
                        group_id=event.group_id,
                        messages=[
                            {
                                "type": "node",
                                "data": {
                                    "name": "\u200b",
                                    "uin": bot.self_id,
                                    "content": msg,
                                },
                            }
                            for msg in msg_list
                        ],
                    )
                except ActionFailed:
                    flag = False
            if not flag:
                for msg in msg_list:
                    await bot.send_group_msg(group_id=event.group_id, message=msg)
