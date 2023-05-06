import time
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.message.element import *
from base.bot import BotUtils
from modules.black_jack_game.base import Poker
from modules.black_jack_game.base import HandCardInfo

async def sendGameStartMessage(groupId: str, hostInfo: str):
    groupInfo = await BotUtils().getBot().get_group(int(groupId))

    time.sleep(0.2)
    await BotUtils().getBot().send_message(
        groupInfo,
        MessageChain(f"那就开始游戏吧，菜菜来当庄家，{hostInfo}"),
    )

async def sendStartGameFailMessage(groupId: str, playerId: str):
    groupInfo = await BotUtils().getBot().get_group(int(groupId))

    time.sleep(0.2)
    await BotUtils().getBot().send_message(
        groupInfo,
        MessageChain([At(int(playerId)), " 已经有游戏在进行啦！"]),
    )

async def sendJoinSuccessMessage(groupId: str, playerId: str, cardInfo: HandCardInfo):
    groupInfo = await BotUtils().getBot().get_group(int(groupId))

    time.sleep(0.2)
    await BotUtils().getBot().send_message(
        groupInfo,
        MessageChain([At(int(playerId)), f" 加入成功，你的手牌是【{cardInfo.toString()}】，轮到你的时候菜菜会提醒你哦～"]),
    )

async def sendPlayerTurnMessage(groupId: str, playerId: str, cardInfo: HandCardInfo):
    groupInfo = await BotUtils().getBot().get_group(int(groupId))

    time.sleep(0.2)
    await BotUtils().getBot().send_message(
        groupInfo,
        MessageChain([At(int(playerId)), f" 轮到你的回合啦！你的手牌是【{cardInfo.toString()}】，{cardInfo.totalValueStr()}请@菜菜发送【要牌】或【停牌】来进行操作哦，30秒内不操作将会被强制停牌哦"]),
    )

async def sendJoinFailMessage(groupId: str, playerId: str, reason: str):
    groupInfo = await BotUtils().getBot().get_group(int(groupId))
    fail = reason
    if fail == "has_joined":
        fail = "你已经在游戏里了哦，轮到你的时候才可以进行操作～"
    elif fail == "no_seat":
        fail = "已经没有位置啦～"
    elif fail == "game_end":
        fail = "游戏正在结束阶段，麻烦下局再来吧～"

    time.sleep(0.2)
    await BotUtils().getBot().send_message(
        groupInfo,
        MessageChain([At(int(playerId)), " 加入失败，", fail]),
    )

async def sendAskCardResultMessage(groupId: str, playerId: str, card: Poker, handInfo: HandCardInfo):
    text = f"你抽到了一张【{card.toString()}】，现在你的手牌是【{handInfo.toString()}】，{handInfo.totalValueStr()}"
    if (handInfo.gameScore() >= 100 or handInfo.gameScore() <= 0):
        text += "你的回合结束了哦～"
    else:
        text += "你可以继续操作啦～"
    groupInfo = await BotUtils().getBot().get_group(int(groupId))

    time.sleep(0.2)
    await BotUtils().getBot().send_message(
        groupInfo,
        MessageChain([At(int(playerId)), text]),
    )

async def sendAskCardFailMessage(groupId: str, playerId: str, reason: str):
    groupInfo = await BotUtils().getBot().get_group(int(groupId))
    fail = reason
    if fail == "no_join":
        fail = "你没有加入游戏哦～"
    elif fail == "no_your_turn":
        fail = "还不是你的回合啦！"

    time.sleep(0.2)
    await BotUtils().getBot().send_message(
        groupInfo,
        MessageChain([At(int(playerId)), " 要牌失败，", fail]),
    )

async def sendStopCardResultMessage(groupId: str, playerId: str):
    groupInfo = await BotUtils().getBot().get_group(int(groupId))

    time.sleep(0.2)
    await BotUtils().getBot().send_message(
        groupInfo,
        MessageChain([At(int(playerId)), " 那就停牌啦，请耐心等待游戏结果～"]),
    )


async def sendStopCardFailMessage(groupId: str, playerId: str, reason: str):
    groupInfo = await BotUtils().getBot().get_group(int(groupId))
    fail = reason
    if fail == "no_join":
        fail = "你没有加入游戏哦～"
    elif fail == "no_your_turn":
        fail = "还不是你的回合啦！"

    time.sleep(0.2)
    await BotUtils().getBot().send_message(
        groupInfo,
        MessageChain([At(int(playerId)), " 停牌失败，", fail]),
    )

async def sendGameResultMessage(groupId: str, total: int, hostTurn: str, successList: list[str]):
    groupInfo = await BotUtils().getBot().get_group(int(groupId))
    await BotUtils().getBot().send_message(
        groupInfo,
        MessageChain(hostTurn),
    )
    messageList = []
    if (len(successList) == 0):
        messageList.append("你们都不是菜菜的对手！")
    elif (len(successList) == total):
        messageList.append("只有菜菜自己输了QAQ？")
    else:
        messageList.append("游戏结束～ 赢家是")
    for player in successList:
        messageList.append(At(int(player)))
        messageList.append(" ")

    time.sleep(0.2)
    await BotUtils().getBot().send_message(
        groupInfo,
        MessageChain(messageList),
    )

async def sendGameTimeoutMessage(groupId: str, playerId: str):
    groupInfo = await BotUtils().getBot().get_group(int(groupId))

    time.sleep(0.2)
    await BotUtils().getBot().send_message(
        groupInfo,
        MessageChain([At(int(playerId)), " 这么久不理菜菜，菜菜不带你玩啦！"])
    )