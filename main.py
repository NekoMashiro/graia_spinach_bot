import pkgutil

from creart import create
from graia.ariadne.app import Ariadne
from graia.ariadne.connection.config import (
    config,
)
from graia.broadcast import Broadcast
from graia.saya import Saya

saya = create(Saya)

def doReloadModules():
    print("============ 重载所有模块 ============")
    # 先删除所有模块
    for channel in saya.channels:
        print("卸载模块" + channel.title)
    print("============ 重新安装全部 ============")
    # 再重新引入所有模块
    with saya.module_context():
        for module_info in pkgutil.iter_modules(["modules"]):
            if module_info.name.startswith("_"):
                continue
            saya.require(f"modules.{module_info.name}")
            print("安装模块" + module_info.name)
    print("============ 重载模块完成 ============")

if __name__ == '__main__':
    # 机器人init
    app = Ariadne(
        connection=config(
            0,  # qq号，好孩子不可以看
            ""  # 密码，好孩子不可以看
        ),
    )
    # 引入所有模块
    doReloadModules()
    # 启动！
    app.launch_blocking()
