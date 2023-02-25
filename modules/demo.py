from graia.ariadne.app import Ariadne
from graia.ariadne.event.message import FriendMessage
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.model import Friend

from graia.saya import Channel
from graia.saya.builtins.broadcast.schema import ListenerSchema

channel = Channel.current()


@channel.use(ListenerSchema(listening_events=[FriendMessage]))
async def setu(app: Ariadne, friend: Friend, message: MessageChain):
    if message.display == "你好":
         await app.send_message(
            friend,
            MessageChain(f"不要说{message.display}，来点涩图"),
         )
