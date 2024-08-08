from datetime import datetime
import os
from nonebot import require, get_bot
require("nonebot_plugin_apscheduler")
from nonebot_plugin_apscheduler import scheduler
from nonebot.adapters.onebot.v11 import Message, MessageSegment

# Utils
from ...utils.bingoInfo import (
    getTodayBingoCustomFramePics,
    getTodayBingoSyogo,
    getTodayBingoCustomFrame,
    getTodayPlateNumber,
)

# 每天0点自动更新Bingo
@scheduler.scheduled_job("cron", hour=0, minute=0, id="autoBingo")
async def autoBingo():
    bot = get_bot()
    todaySyogo = getTodayBingoSyogo()  # 获取今日Bingo称号
    todayCustomFrame = getTodayBingoCustomFrame()  # 获取今日Bingo自定义边框
    todayPlateNumber = getTodayPlateNumber()  # 获取今日车牌号
    todayCustomFramePicSrc = getTodayBingoCustomFramePics()
    date = datetime.now().strftime("%Y/%m/%d")  # 获取今日日期

    content = (
        "今日Bingo奖品已更新！\n"
        f"<{date}>\n"
        f"[称号] {todaySyogo}\n"
        f"[自定义边框] {todayCustomFrame}\n"
        f"[车牌号] {todayPlateNumber}\n"
    )
    image = todayCustomFramePicSrc

    # 组合消息
    message = Message([MessageSegment.text(content), MessageSegment.image(image)])

    # 遍历普通群列表，给全部群发送Bingo更新消息
    normal_group_ids = os.getenv("NORMAL_GROUP_ID", "").strip("[]").replace('"', '').split(", ")
    for normal_group_id in normal_group_ids:
        await bot.send_group_msg(group_id=int(normal_group_id), message=message)