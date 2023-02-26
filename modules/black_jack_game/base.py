import random

class Poker:
    def __init__(self):
        self.color = ""
        self.text = 0

    def blackJackPoint(self) -> int:
        if self.text == "A":
            return 1
        if self.text == "J" or self.text == "Q" or self.text == "K":
            return 10
        return int(self.text)
    
    def toString(self) -> str:
        return f"{self.color}{self.text}"

class HandCardInfo:
    def __init__(self):
        self.pokerlist: list[Poker] = []

    def is_3x7(self) -> bool:
        if len(self.pokerlist) != 3:
            return False
        for poker in self.pokerlist:
            if poker.text != "7":
                return False
        return True
    
    def is_5d(self) -> bool:
        if len(self.pokerlist) < 5:
            return False
        totalValue = 0
        for poker in self.pokerlist:
            totalValue += poker.blackJackPoint()
        return totalValue <= 21

    def is_blackJack(self) -> bool:
        if len(self.pokerlist) != 2:
            return False
        if self.pokerlist[0].blackJackPoint == 1 and self.pokerlist[1] == 10:
            return True
        if self.pokerlist[0].blackJackPoint == 10 and self.pokerlist[1] == 1:
            return True
        return False
    
    def realPoint(self) -> int:
        totalValue = 0
        hasA = False
        for poker in self.pokerlist:
            value = poker.blackJackPoint()
            totalValue += value
            if (value == 1):
                hasA = True
        if hasA and totalValue <= 11:
            totalValue += 11
        return totalValue
            
    def gameScore(self) -> int:
        if self.is_3x7():
            return 10000
        if self.is_5d():
            return 1000
        if self.is_blackJack():
            return 100
        realPoint = self.realPoint()
        if realPoint <= 21:
            return realPoint
        return 0

    def totalValueStr(self) -> str:
        if self.is_3x7():
            return "是三个七耶！"
        if self.is_5d():
            return "五张牌加起来没有超过21点！"
        if self.is_blackJack():
            return "是BlackJack啦！"
        realPoint = self.realPoint()
        if realPoint <= 21:
            return f"合计{realPoint}点～"
        return f"加起来有{realPoint}点，爆牌啦！"
    
    def toString(self) -> str:
        string = ""
        for poker in self.pokerlist:
            if (len(string) > 0):
                string += " "
            string += poker.toString()
        return string

class Deck:
    card_list: list[Poker]

    def __init__(self):
        self.card_list = []
        for color in ["♠️", "♥️", "♣️", "♦️"]:
            for text in ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]:
                poker = Poker()
                poker.color = color
                poker.text = text
                self.card_list.append(poker)
        self.refresh()

    def refresh(self):
        for i in range(1000):
            pos = random.randint(0, len(self.card_list) - 1)
            card = self.card_list.pop(pos)
            self.card_list.append(card)

    def draw(self):
        if len(self.card_list) > 0:
            return self.card_list.pop(0)

