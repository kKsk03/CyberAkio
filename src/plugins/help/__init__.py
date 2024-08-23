import os
from nonebot import on_command
from nonebot.adapters.onebot.v11 import Bot, Event
from nonebot import logger
from nonebot.permission import SuperUser

help = on_command("help", aliases={"HELP"})

helpMenuContent = (
    "=== 帮助菜单 ===\n"
    "[帮助菜单]\n"
    "👉 /help\n"
    "[今日Bingo奖品信息]\n"
    "👉 /bingo\n"
    "[XRS服务器状态]\n"
    "👉 /status\n"
    "[查询用户信息]\n"
    "👉 /info\n"
    "[随机Capoo]\n"
    "👉 capoo"
)

adminHelpMenuContent = (
    "=== 管理员菜单 ===\n"
    "[管理员菜单]\n"
    "👉 /help\n"
    "[生成指定QQ的邀请码]\n"
    "👉 /code <QQ号>\n"
    "[删除指定QQ的邀请码]\n"
    "👉 /delcode <QQ号>\n"
    "[查看所有邀请码]\n"
    "👉 /codelist\n"
    "[查询该QQ号用户信息]\n"
    "👉 /info <QQ号>\n"
    "[查询该OCM的参与玩家列表]\n"
    "👉 /opu <competitionId>"
)

superAdminHelpMenuContent = (
    "=== 超级管理员菜单 ===\n"
    "[超级管理员菜单]\n"
    "👉 /help\n"
    "[增加用户的XR点数]\n"
    "👉 /addxr <userId> <数量>\n"
    "[减少用户的XR点数]\n"
    "👉 /reducexr <userId> <数量>\n"
    "[设置用户的XR点数]\n"
    "👉 /setxr <userId> <数量>\n"
    "[增加用户的抽奖券]\n"
    "👉 /addticket <userId> <数量>\n"
    "[减少用户的抽奖券]\n"
    "👉 /reduceticket <userId> <数量>\n"
    "[设置用户的抽奖券]\n"
    "👉 /setticket <userId> <数量>\n"
)

@help.handle()
async def _(bot: Bot, event: Event):
    print(event.get_event_name())
    if event.get_event_name() == "message.private.friend":
        logger.info("[私聊] /help")
        if (SuperUser()):
            await help.finish(superAdminHelpMenuContent)
        else:
            # 不是超级管理员
            return
    else:
        logger.info("[群聊] /help")
        groupId = str(event.get_session_id().split("_")[1]) # QQ群号
        userId = str(event.get_session_id().split("_")[2]) # QQ号

        if not groupId == os.getenv("ADMIN_GROUP_ID"):
            logger.info("[普通群] /help")
            await help.finish(helpMenuContent)
        else:
            logger.info("[管理群] /help")
            await help.finish(adminHelpMenuContent)
