from nonebot import on_command
from nonebot import logger
import requests

status = on_command("status")


@status.handle()
async def _():
    try:
        response = requests.get('https://w6r-status.xenon-rs.tech/status', timeout=10)
        if response.ok:
            json_response = response.json()
            logger.info(f"Status response: {json_response}")
            if json_response.get("status") is True:
                await status.finish(f"XRS服务器状态\n[状态] 正常")
            else:
                await status.finish(f"XRS服务器状态\n[状态] 维护/故障")
        else:
            await status.finish(f"XRS服务器状态\n[状态] 维护/故障")
    except requests.exceptions.RequestException as e:
        print(e)
        await status.finish(f"XRS服务器状态\n[状态] 维护/故障")