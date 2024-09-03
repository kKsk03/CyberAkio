from datetime import datetime
import os
from nonebot.permission import SuperUser
from nonebot import on_command
from nonebot import logger
from nonebot.adapters.onebot.v11 import Bot, Event, Message, MessageSegment
from nonebot.params import CommandArg
import psycopg2

# SQL
from ...utils.sql import web_db_config, game_db_config

info = on_command("info", force_whitespace=True)

@info.handle()
async def _(bot: Bot, event: Event, args: Message = CommandArg()):
    groupId = None
    userId = None
    if "_" in event.get_session_id():
        logger.info(f"[群聊] {event.get_user_id()} 正在群聊使用/info")
        groupId = str(event.get_session_id().split("_")[1])  # QQ群号
        userId = str(event.get_session_id().split("_")[2])  # QQ号
    else:
        logger.info(f"[私聊] {event.get_user_id()} 正在私聊使用/info")
        groupId = "0" # 这样就可以兼容私聊
        userId = event.get_user_id()

    # 普通群聊
    if not groupId == os.getenv("ADMIN_GROUP_ID") and not groupId == "0":
        # 遍历群组列表检查groupId是否在其中
        normal_group_ids = os.getenv("NORMAL_GROUP_ID", "").strip("[]").replace('"', '').split(", ")
        if not any(groupId == normalGroupId for normalGroupId in normal_group_ids):
            await info.finish("本功能仅限已部署的群内使用！")
            return

        logger.info(f"[普通群] {userId} 正在群 {groupId} 使用/info")
        targetQQNumber = userId

        connection = psycopg2.connect(**web_db_config)
        cursor = connection.cursor()
        cursor.execute(
            'SELECT * FROM public."WebUser" WHERE "userQQ" = %s;',
            (targetQQNumber,),
        )
        webUserResults = cursor.fetchall()
        cursor.close()
        connection.close()

        if not webUserResults:
            await info.finish(
                "没有您的用户信息！\n您没有在XRS网上上注册账号或有卡但没有绑定账号！\n若需绑定请联系管理员！"
            )
            return
        else:
            connection = psycopg2.connect(**game_db_config)
            cursor = connection.cursor()
            cursor.execute(
                'SELECT * FROM public."User" WHERE "id" = %s;',
                (webUserResults[0][1],),
            )
            gameUserResults = cursor.fetchall()
            cursor.close()
            connection.close()
            lastPlayedAt = datetime.fromtimestamp(gameUserResults[0][13]).strftime(
                "%Y/%m/%d %H:%M:%S"
            )
            lastLoginAt = datetime.fromtimestamp(webUserResults[0][7]).strftime(
                "%Y/%m/%d %H:%M:%S"
            )
            content = f"您的用户信息如下：\n[QQ号] {webUserResults[0][3]}\n[用户名] {webUserResults[0][2]}\n[最后登录时间] {lastLoginAt}\n[最后游玩时间] {lastPlayedAt}\n[抽奖券] {webUserResults[0][9]} 张\n[积累抽数] {webUserResults[0][10]} 抽\n[XR点数] {webUserResults[0][11]} 点"
            await info.finish(content)
            return
        
    # 管理员群
    elif groupId == os.getenv("ADMIN_GROUP_ID") and not groupId == "0":  
        logger.info(f"[管理群] {userId} 正在群 {groupId} 使用/info | [参数] {args}")
        await infoCommandAdmin(args)
    elif groupId == "0" and SuperUser():
        logger.info(f"[超级管理员] {userId} 正在私聊使用/info | [参数] {args}")
        await infoCommandAdmin(args)
    else:
        logger.info(f"[权限拦截] {userId} 正在尝试使用/info但被拦截 | [参数] {args}")
        return

async def infoCommandAdmin(args):
    if args.extract_plain_text() == "":
        logger.warning("[管理群] 参数为空！")
        await info.finish("请在指令后输入要查询的QQ号！\n示例：/info 114514")
        return
    else:
        targetQQNumber = args.extract_plain_text()
        if not targetQQNumber.isdigit():
            await info.finish("QQ号必须为数字！\n示例：/info 114514")
            return
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
            connection = psycopg2.connect(**game_db_config)
            cursor = connection.cursor()
            cursor.execute(
                'SELECT * FROM public."User" WHERE "id" = %s;',
                (webUserResults[0][1],),
            )
            gameUserResults = cursor.fetchall()
            cursor.close()
            connection.close()
            # 转换lastPlayedAt时间戳
            lastPlayedAt = datetime.fromtimestamp(gameUserResults[0][13]).strftime(
                "%Y/%m/%d %H:%M:%S"
            )
            # 转换lastLoginAt时间戳
            lastLoginAt = datetime.fromtimestamp(webUserResults[0][7]).strftime(
                "%Y/%m/%d %H:%M:%S"
            )
            banInfo = "正常"
            if gameUserResults[0][5] == True:
                banInfo = "已封禁"
            content = (
                f"=== 用户信息 ===\n[userId] {webUserResults[0][1]}\n[用户QQ] {webUserResults[0][3]}\n[用户名] {webUserResults[0][2]}\n[抽奖券] {webUserResults[0][9]} 张\n[积累抽数] {webUserResults[0][10]} 抽\n[XR点数] {webUserResults[0][11]} 点\n[最后登录时间] {lastLoginAt}\n[最后游玩时间] {lastPlayedAt}\n[最后登录IP] {webUserResults[0][8]}\n[账户状态] {banInfo}\n\n=== 卡号 ===\n[chipId] {gameUserResults[0][1]}\n[accessCode] {gameUserResults[0][2]}",
            )
            # 返回信息
            await info.finish(content)
        else:
            content = (f"QQ {targetQQNumber} 不存在用户信息哦 ~",)
            await info.finish(content)
            return