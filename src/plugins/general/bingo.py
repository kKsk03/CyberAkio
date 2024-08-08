from nonebot import on_command
from nonebot.adapters.onebot.v11 import Message, MessageSegment
from datetime import datetime

# Utils
from ...utils.bingoInfo import (
    getTodayBingoSyogo,
    getTodayBingoCustomFrame,
    getTodayPlateNumber,
    getTodayBingoCustomFramePics
)

bingo = on_command("bingo")


@bingo.handle()
async def _():
    todaySyogo = getTodayBingoSyogo()  # 获取今日Bingo称号
    todayCustomFrame = getTodayBingoCustomFrame()  # 获取今日Bingo自定义边框
    todayPlateNumber = getTodayPlateNumber()  # 获取今日车牌号
    todayCustomFramePicSrc = getTodayBingoCustomFramePics()
    date = datetime.now().strftime("%Y/%m/%d")  # 获取今日日期

    content = (
        "今日Bingo奖品信息如下：\n"
        f"<{date}>\n"
        f"[称号] {todaySyogo}\n"
        f"[自定义边框] {todayCustomFrame}\n"
        f"[车牌号] {todayPlateNumber}\n"
    )
    image = todayCustomFramePicSrc

    # 组合消息
    message = Message([MessageSegment.text(content), MessageSegment.image(image)])

    await bingo.finish(message=message)
