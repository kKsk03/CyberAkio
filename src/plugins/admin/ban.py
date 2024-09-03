import os
from nonebot import on_command
from nonebot import logger
from nonebot.adapters.onebot.v11 import Bot, Event, Message, MessageSegment
from nonebot.params import CommandArg
import psycopg2

# SQL
from ...utils.sql import web_db_config, game_db_config

ban = on_command("ban", force_whitespace=True)
unban = on_command("unban", force_whitespace=True)

@ban.handle()
async def _(bot: Bot, event: Event, args: Message = CommandArg()):
    groupId = str(event.get_session_id().split("_")[1]) # QQ群号
    userQQ = str(event.get_session_id().split("_")[2]) # QQ号

    if not groupId == os.getenv("ADMIN_GROUP_ID"):
        logger.warning(f"[权限拦截] 用户 {userQQ} 正在群 {groupId} 尝试使用/ban指令!")
        return
    
    logger.info(f"[管理群] {groupId} | [/ban] Requester's QQ: {userQQ}")

    if args.extract_plain_text() == "":
        await ban.finish("请在指令后输入QQ号！\n示例：/ban 114514")

    # 检查参数是否为纯数字
    if not args.extract_plain_text().isdigit():
        await ban.finish("userId必须为数字！\n示例：/ban 114514")
        return
        
    targetUserId = args.extract_plain_text() # 指定封禁的userId

    # 检查是否有该用户
    connection = psycopg2.connect(**web_db_config)
    cursor = connection.cursor()
    cursor.execute(
        'SELECT * FROM public."WebUser" WHERE "userId" = %s;',
        (targetUserId,),
    )
    webUserResults = cursor.fetchall()
    cursor.close()
    connection.close()

    if not webUserResults:
        await ban.finish("没有该用户！\n请更换一个UserId!")
        return
    else:
        connection = psycopg2.connect(**game_db_config)
        cursor = connection.cursor()
        cursor.execute(
            'UPDATE public."User" SET "userBanned" = true WHERE "id" = %s;',
            (targetUserId),
        )
        connection.commit()
        cursor.close()
        connection.close()

        await ban.finish(f"UserId: {targetUserId} 已被封禁!")
    
@unban.handle()
async def _(bot: Bot, event: Event, args: Message = CommandArg()):
    groupId = str(event.get_session_id().split("_")[1]) # QQ群号
    userQQ = str(event.get_session_id().split("_")[2]) # QQ号

    if not groupId == os.getenv("ADMIN_GROUP_ID"):
        logger.warning(f"[权限拦截] 用户 {userQQ} 正在群 {groupId} 尝试使用/unban指令!")
        return
    
    logger.info(f"[管理群] {groupId} | [/unban] Requester's QQ: {userQQ}")

    if args.extract_plain_text() == "":
        await unban.finish("请在指令后输入QQ号！\n示例：/unban 114514")

    # 检查参数是否为纯数字
    if not args.extract_plain_text().isdigit():
        await unban.finish("userId必须为数字！\n示例：/unban 114514")
        return
        
    targetUserId = args.extract_plain_text() # 指定解封的userId

    # 检查是否有该用户
    connection = psycopg2.connect(**web_db_config)
    cursor = connection.cursor()
    cursor.execute(
        'SELECT * FROM public."WebUser" WHERE "userId" = %s;',
        (targetUserId,),
    )
    webUserResults = cursor.fetchall()
    cursor.close()
    connection.close()

    if not webUserResults:
        await unban.finish("没有该用户！\n请更换一个UserId!")
        return
    else:
        connection = psycopg2.connect(**game_db_config)
        cursor = connection.cursor()
        cursor.execute(
            'UPDATE public."User" SET "userBanned" = false WHERE "id" = %s;',
            (targetUserId),
        )
        connection.commit()
        cursor.close()
        connection.close()

        await unban.finish(f"UserId: {targetUserId} 已被解封!")

