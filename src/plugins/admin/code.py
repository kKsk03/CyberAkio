import os
from nonebot import on_command
from nonebot import logger
from nonebot.adapters.onebot.v11 import Bot, Event, Message, MessageSegment
from nonebot.params import CommandArg
import psycopg2

# SQL
from ...utils.sql import web_db_config, game_db_config

code = on_command("code", force_whitespace=True)

@code.handle()
async def _(bot: Bot, event: Event, args: Message = CommandArg()):
    groupId = str(event.get_session_id().split("_")[1]) # QQ群号
    userId = str(event.get_session_id().split("_")[2]) # QQ号

    if not groupId == os.getenv("ADMIN_GROUP_ID"):
        logger.warning(f"[权限拦截] 用户 {userId} 正在群 {groupId} 尝试使用/code指令！")
        return

    logger.info(f"[管理群] {groupId} | [/code {args}] Requester's QQ: {userId}")

    if args.extract_plain_text() == "":
        await code.finish("请在指令后输入QQ号！\n示例：/code 114514")

    # 检查参数是否为纯数字
    if not args.extract_plain_text().isdigit():
        await code.finish("QQ号必须为数字！\n示例：/code 114514")
        return
        
    targetQQNumber = args.extract_plain_text() # 生成邀请码的QQ号

    # 检查是否已注册
    connection = psycopg2.connect(**web_db_config)
    cursor = connection.cursor()
    cursor.execute(
        'SELECT * FROM public."WebUser" WHERE "userQQ" = %s;',
        (targetQQNumber,),
    )
    webUserResults = cursor.fetchall()
    cursor.close()
    connection.close()

    if webUserResults:
        logger.warning(f"QQ {targetQQNumber} 已注册！")
        await code.finish(f"QQ {targetQQNumber} 已注册！")
        return

    # 检查是否已有邀请码
    connection = psycopg2.connect(**web_db_config)
    cursor = connection.cursor()
    cursor.execute(
        'SELECT * FROM public."WebUserInviteCode" WHERE "bindQQ" = %s AND "inviteCode" = %s;',
        (targetQQNumber, f"XRS{targetQQNumber}"),
    )
    webUserInviteCodeResults = cursor.fetchall()
    cursor.close()
    connection.close()

    if webUserInviteCodeResults:
        logger.warning(f"QQ {targetQQNumber} 已有邀请码！\n邀请码：XRS{targetQQNumber}")
        await code.finish("QQ已生成邀请码！")
        return

    inviteCode = f"XRS{targetQQNumber}"  # 邀请码
    connection = psycopg2.connect(**web_db_config)
    cursor = connection.cursor()
    cursor.execute('INSERT INTO public."WebUserInviteCode"("inviteCode", "bindQQ") VALUES (%s, %s) RETURNING "dbId";', (inviteCode, targetQQNumber,))
    inserted_dbId = cursor.fetchone()[0]
    connection.commit()
    cursor.close()
    connection.close()
    if inserted_dbId:
        await code.finish(f"已为QQ {targetQQNumber} 生成邀请码！\n邀请码：{inviteCode}")
        return
    else:
        await code.finish(f"邀请码生成失败！")
        return