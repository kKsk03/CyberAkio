import os
from nonebot import on_command
from nonebot.adapters.onebot.v11 import Bot, Event
from nonebot import logger

help = on_command("help", aliases={"HELP"})

helpMenuContent = (
    "=== 帮助菜单 ===\n"
    "/help - 帮助菜单\n"
    "/bingo - 获取今日Bingo奖品信息\n"
    "/status - 查询XRS游戏服务器状态\n"
    "/info - 查询用户信息"
)

adminHelpMenuContent = (
    "=== 管理员菜单 ===\n"
    "/help - 管理员菜单\n"
    "/code <QQ号> - 给该QQ号生成邀请码\n"
    "/delcode <QQ号> - 删除该QQ号的邀请码\n"
    "/codelist - 查看所有邀请码\n"
    "/info <QQ号> - 查询该QQ号用户信息"
    "/opu <competitionId> - 查询该OCM的参与玩家列表"
)

@help.handle()
async def _(bot: Bot, event: Event):
    groupId = str(event.get_session_id().split("_")[1]) # QQ群号
    userId = str(event.get_session_id().split("_")[2]) # QQ号

    if not groupId == os.getenv("ADMIN_GROUP_ID"):
        logger.info("[普通群] /help")
        await help.finish(helpMenuContent)
    else:
        logger.info("[管理群] /help")
        await help.finish(adminHelpMenuContent)
