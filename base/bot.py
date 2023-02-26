from graia.ariadne.app import Ariadne
from graia.ariadne.connection.config import config

class BotUtils:
    instance = None

    def __new__(cls):
        if not cls.instance:
            cls.instance = super(BotUtils, cls).__new__(cls)
            cls.bot = Ariadne(
                connection = config(2485909839, ""),
            )
        return cls.instance
    
    def getBot(self):
        return self.bot
