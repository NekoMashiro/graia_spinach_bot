import pkgutil

from creart import create
from graia.ariadne.app import Ariadne
from graia.ariadne.connection.config import (
    config,
)
from graia.broadcast import Broadcast
from graia.saya import Saya

if __name__ == '__main__':
    # 机器人init
    app = Ariadne(
        connection=config(
            0,  # qq号，好孩子不可以看
            ""  # 密码，好孩子不可以看
        ),
    )
    # 引入所有模块
    saya = create(Saya)
    with saya.module_context():
        for module_info in pkgutil.iter_modules(["modules"]):
            if module_info.name.startswith("_"):
                continue
            saya.require(f"modules.{module_info.name}")
    # 启动！
    app.launch_blocking()
