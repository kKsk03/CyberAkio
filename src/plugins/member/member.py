from nonebot import on_notice, logger
from nonebot.adapters.onebot.v11 import GroupIncreaseNoticeEvent, GroupDecreaseNoticeEvent
from nonebot.adapters.onebot.v11 import Message, Bot

import os
import psycopg2
# SQL
from ...utils.sql import web_db_config, game_db_config

member = on_notice()

@member.handle()
async def _(bot: Bot, event: GroupIncreaseNoticeEvent):
    user = event.get_user_id()
    userInfo = await bot.get_group_member_info(group_id=event.group_id, user_id=user, no_cache=False)
    print(userInfo)
    await member.finish(f'欢迎新人 "{userInfo.get("nickname")}" 加入FLYHIGH XRS!\n[游戏安装] https://a.icnn.cn/yGsXNa\n[官网] https://xenon-rs.tech/\n新用户注册请阅读安装教程中的新卡发行部分！')

@member.handle()
async def _(bot: Bot, event: GroupDecreaseNoticeEvent):


    user = event.get_user_id()

    logger.info(f"[玩家退群数据处理] 玩家 {user} 离开了群聊，开始数据检查......")

    # 是否有邀请码
    isHasInviteCode = False
    # 是否有玩家数据
    isHasUserData = False

    # 检查是否有该玩家的邀请码
    connection = psycopg2.connect(**web_db_config)
    cursor = connection.cursor()
    cursor.execute(
        'SELECT * FROM public."WebUserInviteCode" WHERE "bindQQ" = %s;',
        (user,),
    )
    webUserInviteCodeResults = cursor.fetchall()
    cursor.close()
    connection.close()

    if not webUserInviteCodeResults:
        logger.info(f"[玩家退群数据处理] 玩家 {user} 不存在邀请码")
    else:
        logger.info(f"[玩家退群数据处理] 玩家 {user} 存在邀请码，正在删除......")
        # 删除其邀请码
        connection = psycopg2.connect(**web_db_config)
        cursor = connection.cursor()
        cursor.execute(
            'DELETE FROM public."WebUserInviteCode" WHERE "bindQQ" = %s;',
            (user,),
        )
        connection.commit()
        cursor.close()
        connection.close()
        isHasInviteCode = True # 有邀请码
        logger.info(f"[玩家退群数据处理] 玩家 {user} 的邀请码已删除")

    # 检查该玩家是否有数据
    connection = psycopg2.connect(**web_db_config)
    cursor = connection.cursor()
    cursor.execute(
        'SELECT * FROM public."WebUser" WHERE "userQQ" = %s;',
        (user,),
    )
    webUserResults = cursor.fetchall()
    cursor.close()
    connection.close()

    if not webUserResults:
        logger.info(f"[玩家退群数据处理] 玩家 {user} 不存在数据")
    else:
        # 封号
        connection = psycopg2.connect(**game_db_config)
        cursor = connection.cursor()
        cursor.execute(
            'UPDATE public."User" SET "userBanned"=true WHERE "id" = %s;',
            (user,)
        )
        isHasUserData = True # 有玩家数据
        logger.info(f"[玩家退群数据处理] 玩家 {user} 的数据已封号")

    message = None

    if isHasInviteCode and isHasUserData:
        message = f'玩家 "{user}" 离开了玩家群\n=== 数据检查 ===\n[邀请码] 有\n[玩家数据] 有\n=== 数据处理 ===\n[邀请码] 已删除\n[玩家数据] 已封禁'
    elif isHasInviteCode and not isHasUserData:
        message = f'玩家 "{user}" 离开了玩家群\n=== 数据检查 ===\n[邀请码] 有\n[玩家数据] 无\n=== 数据处理 ===\n[邀请码] 已删除'
    elif not isHasInviteCode and isHasUserData:
        message = f'玩家 "{user}" 离开了玩家群\n=== 数据检查 ===\n[邀请码] 无\n[玩家数据] 有\n=== 数据处理 ===\n[玩家数据] 已封禁'
    else:
        message = f'玩家 "{user}" 离开了玩家群\n=== 数据检查 ===\n[邀请码] 无\n[玩家数据] 无\n=== 数据处理 ===\n无需进行数据处理'
        
    await bot.send_group_msg(group_id=os.getenv("ADMIN_GROUP_ID"), message=message)