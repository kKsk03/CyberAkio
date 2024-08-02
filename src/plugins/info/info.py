from datetime import datetime
import os
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
    groupId = str(event.get_session_id().split("_")[1]) # QQ群号
    userId = str(event.get_session_id().split("_")[2]) # QQ号

    if not groupId == os.getenv("ADMIN_GROUP_ID"):
        logger.info(f"[普通群] {userId} 正在群 {groupId} 使用/info")
        targetQQNumber = userId
        await info.finish("这个功能还在写（悲）")
    else:
        logger.info(f"[管理群] {userId} 正在群 {groupId} 使用/info | [参数] {args}")
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

                content=f"=== 用户信息 ===\n[userId] {webUserResults[0][1]}\n[用户QQ] {webUserResults[0][3]}\n[用户名] {webUserResults[0][2]}\n[抽奖券] {webUserResults[0][9]} 张\n[积累抽数] {webUserResults[0][10]} 抽\n[XR点数] {webUserResults[0][11]} 点\n[最后登录时间] {lastLoginAt}\n[最后游玩时间] {lastPlayedAt}\n[最后登录IP] {webUserResults[0][8]}\n[账户状态] {banInfo}\n\n=== 卡号 ===\n[chipId] {gameUserResults[0][1]}\n[accessCode] {gameUserResults[0][2]}",

                # 返回信息
                await info.finish(content)
            else:
                content=f"QQ {targetQQNumber} 不存在用户信息哦 ~",
                await info.finish(content)
                return