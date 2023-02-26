from creart import create
from graia.saya import Saya
from base.bot import BotUtils

saya = create(Saya)

def doReloadModules():
    print("============ 重载所有模块 ============")
    # 先删除所有模块
    for channel in saya.channels:
        print("卸载模块" + channel.title)
    print("============ 重新安装全部 ============")
    # 再重新引入所有模块
    saya.require(f"modules")
    print("============ 重载模块完成 ============")

if __name__ == '__main__':
    # 引入所有模块
    doReloadModules()
    # 启动！
    BotUtils().getBot().launch_blocking()
