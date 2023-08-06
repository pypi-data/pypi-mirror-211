from typing import Union

from nonebot import require, Bot, logger
from nonebot.exception import ActionFailed
from nonebot.internal.adapter import Event

require("nonebot_plugin_session")

from nonebot_plugin_session import Session, SessionIdType, extract_session

try:
    from nonebot.adapters.qqguild import Bot as QQGuildBot
except ImportError:
    QQGuildBot = None

try:
    from nonebot.adapters.onebot.v11 import Bot as OneBotV11Bot
except ImportError:
    OneBotV11Bot = None


class GetNicknameError(RuntimeError):
    ...


class UnsupportedBotError(GetNicknameError):
    ...


async def get_nickname(session_or_event: Union[Session, Event], bot: Bot, raise_on_failed: bool = False):
    if isinstance(session_or_event, Event):
        session = extract_session(bot, session_or_event)
    else:
        session = session_or_event

    try:
        if QQGuildBot is not None and isinstance(bot, QQGuildBot):
            member = await bot.get_member(guild_id=session.id3, user_id=session.id1)
            return member.nick or session.id1
        elif OneBotV11Bot is not None and isinstance(bot, OneBotV11Bot):
            user_info = await bot.get_group_member_info(group_id=session.id2, user_id=session.id1)
            return user_info["card"] or user_info["nickname"]
        else:
            err_msg = f"获取昵称失败 不支持该Bot类型 session={session} bot=<{bot.type} {bot.self_id}>"
            if raise_on_failed:
                raise UnsupportedBotError(err_msg)
            else:
                logger.warning(err_msg)
                return session.get_id(SessionIdType.USER)
    except ActionFailed as e:
        if raise_on_failed:
            raise e
        else:
            err_msg = f"获取昵称失败 ActionFailed session={session} bot=<{bot.type} {bot.self_id}> exception={e}"
            logger.warning(err_msg)
            return session.get_id(SessionIdType.USER)


__all__ = ("get_nickname", "GetNicknameError", "UnsupportedBotError")
