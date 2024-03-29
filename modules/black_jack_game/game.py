import asyncio
from threading import Lock
from modules.black_jack_game.base import *
from modules.black_jack_game.message_sender import *

class BlackJackGame:
    def __init__(self, groupId, firstPlayerId):
        self.groupId = groupId
        self.deck = Deck()
        self.playerList: list[str] = []
        self.playerInfo: dict[str, HandCardInfo] = {}
        self.hostInfo = HandCardInfo()
        self.current_player = ""
        self.hostInfo.pokerlist.append(self.deck.draw())
        self.hostInfo.pokerlist.append(self.deck.draw())
        # 超时相关
        self.seq = 0
        self.lock = Lock()
        self.isFinish = False

        self.addPlayer(firstPlayerId)

    def hideHostState(self) -> str:
        return f"菜菜的第一张牌是{self.hostInfo.pokerlist[0].toString()}，第二张牌会在游戏结束前不会展示～"

    def addPlayer(self, playerId):
        if playerId in self.playerList:
            return "has_joined", None
        if len(self.playerList) == 6:
            return "no_seat", None
        if self.isFinish:
            return "game_end", None
        self.playerList.append(playerId)
        playerHandInfo = HandCardInfo()
        playerHandInfo.pokerlist.append(self.deck.draw())
        playerHandInfo.pokerlist.append(self.deck.draw())
        self.playerInfo[playerId] = playerHandInfo
        return "", playerHandInfo
    
    async def nextPlayerTurn(self):
        if self.current_player == "":
            self.current_player = self.playerList[0]
        else:
            for i in range(len(self.playerList)):
                if self.current_player == self.playerList[i]:
                    if i == len(self.playerList) - 1:
                        self.seq += 1
                        await self.gameEnd()
                        return
                    else:
                        self.current_player = self.playerList[i + 1]
                        break
        await sendPlayerTurnMessage(self.groupId, self.current_player, self.playerInfo.get(self.current_player))
        self.seq += 1
        asyncio.create_task(self.createTimeout(self.seq, self.current_player))

    async def askCard(self, asker):
        self.lock.acquire()
        if asker not in self.playerList:
            self.lock.release()
            return "no_join"
        playerId = self.current_player
        if playerId != asker:
            self.lock.release()
            return "no_your_turn"
        handInfo = self.playerInfo.get(playerId)
        card = self.deck.draw()
        handInfo.pokerlist.append(card)
 
        await sendAskCardResultMessage(self.groupId, playerId, card, handInfo)
        if handInfo.gameScore() >= 100 or handInfo.gameScore() <= 0:
            await self.nextPlayerTurn()
        else:
            self.seq += 1
            asyncio.create_task(self.createTimeout(self.seq, playerId))
        self.lock.release()
        return ""
    
    async def stopCard(self, asker):
        self.lock.acquire()
        if asker not in self.playerList:
            self.lock.release()
            return "no_join"
        playerId = self.current_player
        if playerId != asker:
            self.lock.release()
            return "no_your_turn"
 
        await sendStopCardResultMessage(self.groupId, playerId)
        self.lock.release()
        await self.nextPlayerTurn()

    async def gameEnd(self):
        self.isFinish = True
        # 庄家要牌流程
        text = f"所有人的回合都结束啦，菜菜的另一张卡是【{self.hostInfo.pokerlist[1].toString()}】！加上之前的【{self.hostInfo.pokerlist[0].toString()}】，{self.hostInfo.totalValueStr()}\n"
        while self.hostInfo.gameScore() < 17 and self.hostInfo.gameScore() > 0:
            card = self.deck.draw()
            self.hostInfo.pokerlist.append(card)
            text += f"菜菜要牌！我抽到的牌是【{card.toString()}】！"
            text += f"当前手牌是【{self.hostInfo.toString()}】，{self.hostInfo.totalValueStr()}\n"
        text += "停牌！"
        # 得分比较流程
        successList = []
        for player in self.playerList:
            score = self.playerInfo.get(player).gameScore()
            if score > 0 and score > self.hostInfo.gameScore():
                successList.append(player)

        await sendGameResultMessage(self.groupId, len(self.playerList), text, successList)
        import modules.black_jack_game.game_manager
        modules.black_jack_game.game_manager.removeGameFromManager(self.groupId)

    async def createTimeout(self, seq: int, playerId: str):
        await asyncio.sleep(30)
        if seq == self.seq:
            self.lock.acquire()
            await sendGameTimeoutMessage(self.groupId, playerId)
            await self.nextPlayerTurn()
            self.lock.release()
