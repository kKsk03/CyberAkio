from nonebot import require, get_bot, get_adapter
require("nonebot_plugin_apscheduler")
from nonebot_plugin_apscheduler import scheduler
from nonebot.adapters.onebot.v11 import Message, MessageSegment

@scheduler.scheduled_job("interval", seconds=2, id="autoBingo")
async def autoBingo():
    bot = get_bot()
    print("autoTaskBingo!")
    content = "测试"
    print(await bot.call_api(api="send_group_msg", group_id=246142027, message=Message([MessageSegment.text(content)])))