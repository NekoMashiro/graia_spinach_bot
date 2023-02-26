from importlib.resources import contents
from graia.ariadne.app import Ariadne
from graia.ariadne.event.message import GroupMessage
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.message.element import *
from graia.ariadne.message.parser.base import MentionMe
from graia.ariadne.model import Group
from graia.saya import Channel
from graia.saya.builtins.broadcast.schema import ListenerSchema

from modules.black_jack_game.game_manager import BlackJackGameManager

black_jack_cmd_dict = {
    "来把21点": "game_start",
    "我也要玩21点": "join_game",
    "要牌": "ask_card",
    "停牌": "stop_card",
}

channel = Channel.current()

@channel.use(ListenerSchema(listening_events=[GroupMessage], decorators=[MentionMe()]))
async def black_jack_message(app: Ariadne, group: Group, member: Member, message: MessageChain):
    cmd: str = ""
    list: List = message.content
    if isinstance(list[0], Plain):
        cmd = list[0].text
    elif len(list) > 0 and isinstance(list[1], Plain):
        cmd = list[1].text

    funname = ""
    for item in black_jack_cmd_dict.items():
        if item[0] in cmd:
            funname = item[1]
            break

    if funname == "":
        return
    elif funname == "game_start":
        await BlackJackGameManager().startGame(str(group.id), str(member.id))
    elif funname == "join_game":
        await BlackJackGameManager().joinGame(str(group.id), str(member.id))
    elif funname == "ask_card":
        await BlackJackGameManager().askCard(str(group.id), str(member.id))
    elif funname == "stop_card":
        await BlackJackGameManager().stopCard(str(group.id), str(member.id))
