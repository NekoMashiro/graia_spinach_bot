from modules.black_jack_game.game import BlackJackGame
from modules.black_jack_game.message_sender import *

class BlackJackGameManager:
    instance = None

    def __new__(cls):
        if not cls.instance:
            cls.instance = super(BlackJackGameManager, cls).__new__(cls)
            cls.groupGameDict: dict[str, BlackJackGame] = {}
        return cls.instance

    async def startGame(self, groupId: str, playerId: str):
        if self.groupGameDict.get(groupId) != None:
            await sendStartGameFailMessage(groupId, playerId)
            return
        game = BlackJackGame(groupId, playerId)
        self.groupGameDict[groupId] = game
        await sendGameStartMessage(groupId, game.hideHostState())
        await game.nextPlayerTurn()

    async def joinGame(self, groupId: str, playerId: str):
        result = await self.groupGameDict.get(groupId).addPlayer(playerId)
        if (result == ""):
            await sendJoinSuccessMessage(groupId, playerId)
        else:
            await sendJoinFailMessage(groupId, playerId, result)

    async def askCard(self, groupId: str, playerId: str):
        result = await self.groupGameDict.get(groupId).askCard(playerId)
        if (result != ""):
            await sendAskCardFailMessage(groupId, playerId, result)

    async def stopCard(self, groupId: str, playerId: str):
        await self.groupGameDict.get(groupId).stopCard(playerId)

def removeGameFromManager(groupId: str):
    BlackJackGameManager().groupGameDict.pop(groupId)
