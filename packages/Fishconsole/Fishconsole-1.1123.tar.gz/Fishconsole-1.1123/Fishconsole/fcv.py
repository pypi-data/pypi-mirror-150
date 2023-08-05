def version():
    return '1.1123'

# 它的一切发展都只是为了制作易用中文辅助模块

# 欢迎您进入Fishconsole的调试控制模块，如果您想了解这个集合是如何运行的，请将mod的参数改为False
# ，相信我，输出的内容可能会很多，它们能帮你了解这个模块核心组件的全部运行过程，我呢，只是一个职高生，做这
# 个完全是为爱发电，所以，虽然我的模块不会很好，但正在努力前行——鱼几斤（2022/4/24）
def f_debug(mod=True):
    if mod:
        return {
            "updata": True,
            "Fl": False,
            "PI": True,
            "ZUI": True,
            "UPI": True,
            "cache": True,
            "filecheck": True
        }
    else:

        # 调试模式状态
        # updata True是激活强制更新，False是关闭更新
        # FI 系统日志总开关,Ture是开启，False是关闭
        # pl    False是允许password模块输出消息，True是不允许输出消息
        # ZUI  False是允许字符串转unicode模块输出消息，True是不允许输出消息
        # UPI  False是允许强制更新输出消息，Ture是不允许输出消息
        # cache False是允许缓存模块输出消息，Ture是不允许输出消息
        # filecheck False是允许文件存在性检测输出消息，Ture是不允许输出消息
        return {
            "updata": False,
            "Fl": True,
            "PI": False,
            "ZUI": True,
            "UPI": True,
            "cache": True,
            "filecheck": True
        }
