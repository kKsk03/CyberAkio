import os
from nonebot import on_command
from nonebot import logger
from nonebot.adapters.onebot.v11 import Bot, Event, Message, MessageSegment
from nonebot.params import CommandArg
import psycopg2

# SQL
from ...utils.sql import web_db_config, game_db_config

delcode = on_command("delcode", force_whitespace=True)

@delcode.handle()
async def _(bot: Bot, event: Event, args: Message = CommandArg()):
    groupId = str(event.get_session_id().split("_")[1]) # QQ群号
    userId = str(event.get_session_id().split("_")[2]) # QQ号

    if not groupId == os.getenv("ADMIN_GROUP_ID"):
        logger.warning(f"[权限拦截] 用户 {userId} 正在群 {groupId} 尝试使用/code指令！")
        return
    
    logger.info(f"[管理群] {groupId} | [/delcode {args}] Requester's QQ: {userId}")

    if args.extract_plain_text() == "":
        await delcode.finish("请在指令后输入您要删除的邀请码的QQ号：\n示例：/delcode 114514")

    targetQQNumber = args.extract_plain_text() # 删除邀请码的QQ号

    # 检查该邀请码是否存在
    connection = psycopg2.connect(**web_db_config)
    cursor = connection.cursor()
    cursor.execute(
        'SELECT * FROM public."WebUserInviteCode" WHERE "bindQQ" = %s AND "inviteCode" = %s;',
        (targetQQNumber, f"XRS{targetQQNumber}"),
    )
    inviteCodeResults = cursor.fetchall()
    cursor.close()
    connection.close()

    if inviteCodeResults:
        connection = psycopg2.connect(**web_db_config)
        cursor = connection.cursor()
        cursor.execute('DELETE FROM public."WebUserInviteCode" WHERE "dbId" = %s', (inviteCodeResults[0][0],))
        connection.commit()
        cursor.close()
        connection.close()
        await delcode.finish(f"已成功删除QQ {targetQQNumber} 的邀请码!\n被删除的邀请码：XRS{targetQQNumber}")
        return
    else:
        await delcode.finish("该邀请码不存在！")
        return