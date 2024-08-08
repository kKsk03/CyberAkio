from nonebot import on_command
from nonebot.adapters.onebot.v11 import Bot, Event, Message, MessageSegment
from nonebot.params import CommandArg
import psycopg2
import os
from ...utils.sql import web_db_config, game_db_config
from nonebot.log import logger

opu = on_command("opu")

@opu.handle()
async def _(bot: Bot, event: Event, args: Message = CommandArg()):
    groupId = str(event.get_session_id().split("_")[1]) # QQ群号
    userId = str(event.get_session_id().split("_")[2]) # QQ号

    if not groupId == os.getenv("ADMIN_GROUP_ID"):
        logger.warning(f"[权限拦截] 用户 {userId} 正在群 {groupId} 尝试使用/opu指令！")
        return

    logger.info(f"[管理群] {groupId} | [/opu {args}] Requester's QQ: {userId}")

    if args.extract_plain_text() == "":
        await opu.finish("请在指令后输入要查询的ocmId: \n示例：/opu 1")

    ocmId = args.extract_plain_text()

    connection = psycopg2.connect(**game_db_config)
    cursor = connection.cursor()
    cursor.execute(
        'WITH RankedResults AS (SELECT RANK() OVER (ORDER BY o.result DESC) as rank, c."userId", o."carId", o."dbId", o."competitionId", o."periodId", o.result, o."tunePower", o."tuneHandling", ROW_NUMBER() OVER (PARTITION BY c."userId" ORDER BY o.result DESC) as rn FROM public."OCMTally" o JOIN public."Car" c ON o."carId" = c."carId" WHERE o."competitionId" = %s) SELECT rank, "userId", "carId", "dbId", "competitionId", "periodId", result, "tunePower", "tuneHandling" FROM RankedResults WHERE rn = 1 ORDER BY result DESC;',
        (ocmId,)
    )
    results = cursor.fetchall()
    cursor.close()
    connection.close()

    if results:
        # 循环拼接成字符串，result[0][1] / result[1][1] / result[2][1]等...，每一行显示一条数据
        # 例如邀请码的：invite_codes = "\n".join([f"QQ号：{row[0]}\n邀请码：{row[1]}\n" for row in webUserInviteCodeResults])

        resultsContent = "".join([f"[userId] {row[1]}\n[排名] {row[0]} | [carId] {row[2]}\n" for row in results])
        allUserIdContent = ", ".join([f"{row[1]}" for row in results])

        content = f"查询结果：\n<competitionId: {ocmId}>\n{resultsContent}\n=== 汇总 ===\n[总参与人数] {len(results)} 人\n[参与的userId] \n【{allUserIdContent}】\n=== 备注 ===\n1. 排名显示为该carId的排名，也是该用户最高的排名\n2. 参与的userId按排名从小到大顺序排列"
        await opu.finish(content)
    else:
        await opu.finish("该OCM暂无参与玩家")