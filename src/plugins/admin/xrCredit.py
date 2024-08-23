import os
from nonebot.permission import SuperUser
from nonebot import on_command
from nonebot.rule import to_me
from nonebot.adapters.onebot.v11 import Bot, Event, Message, MessageSegment
from nonebot.params import CommandArg, ArgPlainText

import psycopg2
from ...utils.sql import web_db_config, game_db_config

addxr = on_command("addxr", rule=to_me(), permission=SuperUser(), force_whitespace=True)
reducexr = on_command(
    "reducexr", rule=to_me(), permission=SuperUser(), force_whitespace=True
)
setxr = on_command("setxr", rule=to_me(), permission=SuperUser(), force_whitespace=True)


@addxr.handle()
async def _(bot: Bot, event: Event, args: Message = CommandArg()):
    # 定义参数
    targetUserId = None
    addXRCreditNumber = None

    # 提取并分割参数
    plain_text = args.extract_plain_text()
    if plain_text:
        params = plain_text.split()
        if len(params) == 2:
            param1, param2 = params
            targetUserId = param1
            addXRCreditNumber = param2
        else:
            await addxr.finish("无法执行指令！\n请写入两个参数：\n示例：/addxr 1 1000")
    else:
        await addxr.finish("无法执行指令！\n请写入两个参数：\n示例：/addxr 1 1000")

    # 给指定用户添加信用值
    connection = psycopg2.connect(**web_db_config)
    cursor = connection.cursor()
    cursor.execute(
        'UPDATE public."WebUser" SET "xrCredit"="xrCredit" + %s WHERE "userId" = %s;',
        (addXRCreditNumber, targetUserId),
    )
    connection.commit()
    cursor.close()
    connection.close()

    # 获取指定用户的信用值
    connection = psycopg2.connect(**web_db_config)
    cursor = connection.cursor()
    cursor.execute(
        'SELECT "xrCredit" FROM public."WebUser" WHERE "userId" = %s;',
        (targetUserId,),
    )
    gameResults = cursor.fetchall()
    cursor.close()
    connection.close()

    await addxr.finish(
        f"指定userId：{targetUserId} 的XR点数已增加 {addXRCreditNumber} 点\n该用户当前XR点数：{gameResults[0][0]} 点"
    )


@reducexr.handle()
async def _(bot: Bot, event: Event, args: Message = CommandArg()):
    # 定义参数
    targetUserId = None
    reduceXRCreditNumber = None

    # 提取并分割参数
    plain_text = args.extract_plain_text()
    if plain_text:
        params = plain_text.split()
        if len(params) == 2:
            param1, param2 = params
            targetUserId = param1
            reduceXRCreditNumber = param2
        else:
            await reducexr.finish(
                "无法执行指令！\n请写入两个参数：\n示例：/reducexr 1 1000"
            )
    else:
        await reducexr.finish(
            "无法执行指令！\n请写入两个参数：\n示例：/reducexr 1 1000"
        )

    # 给指定用户减少信用值
    connection = psycopg2.connect(**web_db_config)
    cursor = connection.cursor()
    cursor.execute(
        'UPDATE public."WebUser" SET "xrCredit"="xrCredit" - %s WHERE "userId" = %s;',
        (reduceXRCreditNumber, targetUserId),
    )
    connection.commit()
    cursor.close()
    connection.close()

    # 获取指定用户的信用值
    connection = psycopg2.connect(**web_db_config)
    cursor = connection.cursor()
    cursor.execute(
        'SELECT "xrCredit" FROM public."WebUser" WHERE "userId" = %s;',
        (targetUserId,),
    )
    gameResults = cursor.fetchall()
    cursor.close()
    connection.close()

    await reducexr.finish(
        f"指定userId：{targetUserId} 的XR点数已减少 {reduceXRCreditNumber} 点\n该用户当前XR点数：{gameResults[0][0]} 点"
    )


@setxr.handle()
async def _(bot: Bot, event: Event, args: Message = CommandArg()):
    # 定义参数
    targetUserId = None
    setXRCreditNumber = None

    # 提取并分割参数
    plain_text = args.extract_plain_text()
    if plain_text:
        params = plain_text.split()
        if len(params) == 2:
            param1, param2 = params
            targetUserId = param1
            setXRCreditNumber = param2
        else:
            await setxr.finish("无法执行指令！\n请写入两个参数：\n示例：/setxr 1 1000")
    else:
        await setxr.finish("无法执行指令！\n请写入两个参数：\n示例：/setxr 1 1000")

    # 给指定用户设置信用值
    connection = psycopg2.connect(**web_db_config)
    cursor = connection.cursor()
    cursor.execute(
        'UPDATE public."WebUser" SET "xrCredit" = %s WHERE "userId" = %s;',
        (setXRCreditNumber, targetUserId),
    )
    connection.commit()
    cursor.close()
    connection.close()

    # 获取指定用户的信用值
    connection = psycopg2.connect(**web_db_config)
    cursor = connection.cursor()
    cursor.execute(
        'SELECT "xrCredit" FROM public."WebUser" WHERE "userId" = %s;',
        (targetUserId,),
    )
    gameResults = cursor.fetchall()
    cursor.close()
    connection.close()

    await setxr.finish(
        f"指定userId：{targetUserId} 的XR点数已设置为 {setXRCreditNumber} 点\n该用户当前XR点数：{gameResults[0][0]} 点"
    )
