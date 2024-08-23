import os
from nonebot.permission import SuperUser
from nonebot import on_command
from nonebot.rule import to_me
from nonebot.adapters.onebot.v11 import Bot, Event, Message, MessageSegment
from nonebot.params import CommandArg, ArgPlainText

import psycopg2
from ...utils.sql import web_db_config, game_db_config

addticket = on_command(
    "addticket", rule=to_me(), permission=SuperUser(), force_whitespace=True
)
reduceticket = on_command(
    "reduceticket", rule=to_me(), permission=SuperUser(), force_whitespace=True
)
setticket = on_command(
    "setticket", rule=to_me(), permission=SuperUser(), force_whitespace=True
)

@addticket.handle()
async def _(bot: Bot, event: Event, args: Message = CommandArg()):
    # 定义参数
    targetUserId = None
    addTicketNumber = None

    # 提取并分割参数
    plain_text = args.extract_plain_text()
    if plain_text:
        params = plain_text.split()
        if len(params) == 2:
            param1, param2 = params
            targetUserId = param1
            addTicketNumber = param2
        else:
            await addticket.finish("无法执行指令！\n请写入两个参数：\n示例：/addticket 1 10")
    else:
        await addticket.finish("无法执行指令！\n请写入两个参数：\n示例：/addticket 1 10")

    # 给指定用户添加抽奖券
    connection = psycopg2.connect(**web_db_config)
    cursor = connection.cursor()
    cursor.execute(
        'UPDATE public."WebUser" SET "lotteryTicket"="lotteryTicket" + %s WHERE "userId" = %s;',
        (addTicketNumber, targetUserId),
    )
    connection.commit()
    cursor.close()
    connection.close()

    # 获取指定用户的抽奖券
    connection = psycopg2.connect(**web_db_config)
    cursor = connection.cursor()
    cursor.execute(
        'SELECT "lotteryTicket" FROM public."WebUser" WHERE "userId" = %s;',
        (targetUserId,),
    )
    gameResults = cursor.fetchall()
    cursor.close()
    connection.close()

    await addticket.finish(
        f"指定userId：{targetUserId} 的抽奖券已增加 {addTicketNumber} 张\n该用户当前抽奖券数：{gameResults[0][0]} 张"
    )


@reduceticket.handle()
async def _(bot: Bot, event: Event, args: Message = CommandArg()):
    # 定义参数
    targetUserId = None
    reduceTicketNumber = None

    # 提取并分割参数
    plain_text = args.extract_plain_text()
    if plain_text:
        params = plain_text.split()
        if len(params) == 2:
            param1, param2 = params
            targetUserId = param1
            reduceTicketNumber = param2
        else:
            await reduceticket.finish("无法执行指令！\n请写入两个参数：\n示例：/reduceticket 1 10")
    else:
        await reduceticket.finish("无法执行指令！\n请写入两个参数：\n示例：/reduceticket 1 10")

    # 给指定用户添加抽奖券
    connection = psycopg2.connect(**web_db_config)
    cursor = connection.cursor()
    cursor.execute(
        'UPDATE public."WebUser" SET "lotteryTicket"="lotteryTicket" - %s WHERE "userId" = %s;',
        (reduceTicketNumber, targetUserId),
    )
    connection.commit()
    cursor.close()
    connection.close()

    # 获取指定用户的抽奖券
    connection = psycopg2.connect(**web_db_config)
    cursor = connection.cursor()
    cursor.execute(
        'SELECT "lotteryTicket" FROM public."WebUser" WHERE "userId" = %s;',
        (targetUserId,),
    )
    gameResults = cursor.fetchall()
    cursor.close()
    connection.close()

    await reduceticket.finish(
        f"指定userId：{targetUserId} 的抽奖券已减少 {reduceTicketNumber} 张\n该用户当前抽奖券数：{gameResults[0][0]} 张"
    )


@setticket.handle()
async def _(bot: Bot, event: Event, args: Message = CommandArg()):
    # 定义参数
    targetUserId = None
    setTicketNumber = None

    # 提取并分割参数
    plain_text = args.extract_plain_text()
    if plain_text:
        params = plain_text.split()
        if len(params) == 2:
            param1, param2 = params
            targetUserId = param1
            setTicketNumber = param2
        else:
            await setticket.finish("无法执行指令！\n请写入两个参数：\n示例：/setticket 1 10")
    else:
        await setticket.finish("无法执行指令！\n请写入两个参数：\n示例：/setticket 1 10")

    # 给指定用户添加抽奖券
    connection = psycopg2.connect(**web_db_config)
    cursor = connection.cursor()
    cursor.execute(
        'UPDATE public."WebUser" SET "lotteryTicket"=%s WHERE "userId" = %s;',
        (setTicketNumber, targetUserId),
    )
    connection.commit()
    cursor.close()
    connection.close()
    
    # 获取指定用户的抽奖券
    connection = psycopg2.connect(**web_db_config)
    cursor = connection.cursor()
    cursor.execute(
        'SELECT "lotteryTicket" FROM public."WebUser" WHERE "userId" = %s;',
        (targetUserId,),
    )
    gameResults = cursor.fetchall()
    cursor.close()
    connection.close()

    await setticket.finish(f"指定userId：{targetUserId} 的抽奖券已设置为 {setTicketNumber} 张\n该用户当前抽奖券数：{gameResults[0][0]} 张")