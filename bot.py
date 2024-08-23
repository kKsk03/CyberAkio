import nonebot
from nonebot.adapters.onebot.v11 import Adapter as OnebotAdapter

# 初始化 NoneBot
nonebot.init()

# 注册适配器
driver = nonebot.get_driver()
driver.register_adapter(OnebotAdapter)

# 在这里加载插件
nonebot.load_builtin_plugins("echo")  # 内置插件
nonebot.load_plugin("nonebot_plugin_capoo")  # 第三方插件
nonebot.load_plugins("src/plugins")  # 本地插件

app = nonebot.get_asgi()

if __name__ == "__main__":
    nonebot.run()