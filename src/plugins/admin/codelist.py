import os
from nonebot import on_command
from nonebot import logger
from nonebot.adapters.onebot.v11 import Bot, Event, Message, MessageSegment
from nonebot.params import CommandArg
import psycopg2

# SQL
from ...utils.sql import web_db_config, game_db_config

codelist = on_command("codelist", force_whitespace=True)

@codelist.handle()
async def _(bot: Bot, event: Event):
    groupId = str(event.get_session_id().split("_")[1]) # QQ群号
    userId = str(event.get_session_id().split("_")[2]) # QQ号

    if not groupId == os.getenv("ADMIN_GROUP_ID"):
        logger.warning(f"[权限拦截] 用户 {userId} 正在群 {groupId} 尝试使用/codelist指令！")
        return
    
    logger.info(f"[管理群] {groupId} | [/codelist] Requester's QQ: {userId}")

    connection = psycopg2.connect(**web_db_config)
    cursor = connection.cursor()
    cursor.execute(
        'SELECT "bindQQ", "inviteCode" FROM public."WebUserInviteCode"',
    )
    webUserInviteCodeResults = cursor.fetchall()
    cursor.close()
    connection.close()

    if webUserInviteCodeResults:
        invite_codes = "\n".join([f"QQ号：{row[0]}\n邀请码：{row[1]}\n" for row in webUserInviteCodeResults])
        await codelist.finish("当前已生成的邀请码如下：\n" + invite_codes)
        return
    else:
        await codelist.finish("当前没有邀请码！")
        return