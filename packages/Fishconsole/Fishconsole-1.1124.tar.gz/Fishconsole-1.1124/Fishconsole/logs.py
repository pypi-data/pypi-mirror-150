# ecoding=utf-8


from Fishconsole import fcv


def 颜色(text, 色选="None"):
    if 色选 == "紫色":
        return f"\033[35m{text}\033[0m"
    elif 色选 == "红色":
        return f"\033[31m{text}\033[0m"
    elif 色选 == "黄色":
        return f"\033[33m{text}\033[0m"
    elif 色选 == "蓝色":
        return f"\033[34m{text}\033[0m"
    elif 色选 == "青色":
        return f"\033[36m{text}\033[0m"
    elif 色选 == "绿色":
        return f"\033[32m{text}\033[0m"
    elif 色选 == "红背":
        return f'\033[41m{text}\033[0m'
    elif 色选 == "黄背":
        return f'\033[43m{text}\033[0m'
    elif 色选 == "蓝背":
        return f'\033[44m{text}\033[0m'
    elif 色选 == "绿背":
        return f'\033[42m{text}\033[0m'
    elif 色选 == "紫背":
        return f'\033[45m{text}\033[0m'
    elif 色选 == "青背":
        return f'\033[46m{text}\033[0m'
    else:
        return f"{text}"


# 必须使用return的方式输出，其他的方法输出染色将失去效果
# 我也不知道这是为什么，但是它就是这样，我靠，麻了
def 输入(text, 色选="红色"):
    res = input(f"{颜色('O', f'{色选}')} 》{text}  {颜色('||》', 色选)}")
    return res


def 日志(text, 色选="Nona"):
    if 色选 != "Nona":
        import time
        return 颜色(str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())) + str(f":{text}"), 色选=色选)
    else:
        import time
        return str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())) + str(f":{text}")


# 先导入参数，一个是updata的参数FI

FI = fcv.f_debug()
FI = FI["Fl"]


# 新建这个函数，默认情况下所有的项目都不会运行，通过传递的参数开启相应的功能（其实都一样）
def 系统日志(text, 参数=False):
    if FI:
        import time
        # 我想精简这个东西，就是用逻辑表达式，如果其中一个条件满足，那就开启这个，但是它只开启一次，下一个使用这个东西传递的参数和自己的参数不一样的话就不开
        # 现在我要的是默认输出，遇到情况就来个无效语句
        if 参数:
            # 这是True时执行的，默认情况下不会执行，但是这里会有一个地方需要注意一下，因为
            # 参数被改了，所以当参数没有被再次更改为False之前其中的任何跟系统日志有关的内容就不会被输出
            1 + 1
        else:
            a = 颜色(f"Fishconsole{fcv.version()}" + "》" + str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())),
                   色选="紫色") + str(f":{text}")
            print(a)


def 分割线(标题, text, 色选="Nona"):
    if 色选 != "Nona":
        import time
        return "\n\n\n\n\n\n" + 颜色(f"- {标题} -", 色选=色选) + f"  {text}:\n--------------------------\n"
    else:
        return f"\n\n\n\n\n\n- {标题} -  {text}:\n--------------------------\n"


def 错误跟踪(路径: list, 内容: str, 参数):
    res = "||"
    for a in 路径:
        res = res + "》" + a
    res = res + "》" + ":" + 内容 + " [" + 参数 + "]"
    raise NotImplementedError(res)


def 变量查看(变量名: str, 变量, 色选: str = "红色"):
    print("="*63)
    print(日志(f"  ||（{颜色('变量名', 色选)}：{变量名}）（{颜色('数据', 色选)}：{变量}）（{颜色('类型', 色选)}: {type(变量)}）||"))
    print("="*63+"\n\n")


# print(日志(123, 色选="红色"))
# print(分割线("123","456","红色"))
# 全局参数="红色"
# a = finput("你你你你你你像个傻逼一样", 全局参数)
# 错误跟踪(["Fishconsole", "logs", "错误跟踪"], "笑死了","哈哈哈")
系统日志("用户调用了logs模块")
