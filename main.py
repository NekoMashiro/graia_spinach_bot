from creart import create
from graia.ariadne.app import Ariadne
from graia.ariadne.connection.config import (
    HttpClientConfig,
    WebsocketClientConfig,
    config,
)
from graia.ariadne.event.message import FriendMessage
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.model import Friend
from graia.broadcast import Broadcast

bcc = create(Broadcast)
app = Ariadne(
    connection=config(
        0,  # qq号，好孩子不可以看
        ""  # 密码，好孩子不可以看
    ),
)


@bcc.receiver(FriendMessage)
async def setu(app: Ariadne, friend: Friend, message: MessageChain):
    if message.display == "你好":
        await app.send_message(
            friend,
            MessageChain(f"不要说{message.display}，来点涩图"),
        )


app.launch_blocking()
