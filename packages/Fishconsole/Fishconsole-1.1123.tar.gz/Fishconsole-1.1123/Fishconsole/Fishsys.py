from Fishconsole import fcv
from Fishconsole import logs
from Fishconsole import helps

logs.系统日志("用户调用了tool模块")
# 导入强制更新系统所需要的内容
PI = fcv.f_debug()
PI = PI["PI"]
ZUI = fcv.f_debug()
ZUI = ZUI["ZUI"]
cache = fcv.f_debug()
cache = cache["cache"]
filecheck = fcv.f_debug()
filecheck = filecheck["filecheck"]


# 这是一座屎山，能修则修，不能修就算了
# 模式,加密密码,内容
def passwordsys(模式: any, id_protect: str, password_a: str):
    import re
    import base64
    password = str(password_a)
    password_a = str(password_a)
    id_protect = str(id_protect)

    def encrypt(en_str):
        en_str = base64.b64encode(bytes(en_str, "utf-8"))
        return en_str.decode("utf-8")

    def decrypt(de_str):
        de_str = base64.b64decode(de_str.encode("utf-8"))
        return de_str.decode("utf-8")

    模式 = str(模式)
    if 模式 == "1":
        logs.系统日志("判断用户输入的值有没有致命问题,顺便拼接一下内容", PI)
        res_a = ""
        res_b = ""
        for a in password:
            res_a = res_a + a
            if a == "@":
                print(logs.颜色(logs.日志("你的密码中不允许有@符号，请重新输入"), 色选="红色"))
                exit()

        for b in id_protect:
            res_b = res_b + b
            if b == "@":
                print(logs.颜色(logs.日志("你的原文中不允许有@符号，请重新输入"), 色选="红色"))
                exit()
        else:
            logs.系统日志("确认成功", PI)
        logs.系统日志("转移变量的数据", PI)
        password = res_b
        id_protect = res_a
        logs.系统日志("拼接用户输入的内容", PI)
        res = password + "@" + id_protect
        logs.系统日志("对用户输入的内容进行加密", PI)
        jiami_last = ""
        count = 0
        counta = 0
        for a in res:
            counta = counta + 1
            if a == "1":
                jiami_last = jiami_last + "aaa"
                count = count + 1
            if a == "2":
                jiami_last = jiami_last + "aab"
                count = count + 1
            if a == "3":
                jiami_last = jiami_last + "aac"
                count = count + 1
            if a == "4":
                jiami_last = jiami_last + "aad"
                count = count + 1
            if a == "5":
                jiami_last = jiami_last + "aae"
                count = count + 1
            if a == "6":
                jiami_last = jiami_last + "aaf"
                count = count + 1
            if a == "7":
                jiami_last = jiami_last + "aba"
                count = count + 1
            if a == "8":
                jiami_last = jiami_last + "abb"
                count = count + 1
            if a == "9":
                jiami_last = jiami_last + "abc"
                count = count + 1
            if a == "0":
                jiami_last = jiami_last + "abd"
                count = count + 1
            if a == "a":
                jiami_last = jiami_last + "abe"
                count = count + 1
            if a == "b":
                jiami_last = jiami_last + "abf"
                count = count + 1
            if a == "c":
                jiami_last = jiami_last + "aca"
                count = count + 1
            if a == "d":
                jiami_last = jiami_last + "acb"
                count = count + 1
            if a == "e":
                jiami_last = jiami_last + "acc"
                count = count + 1
            if a == "f":
                jiami_last = jiami_last + "acd"
                count = count + 1
            if a == "g":
                jiami_last = jiami_last + "ace"
                count = count + 1
            if a == "h":
                jiami_last = jiami_last + "acf"
                count = count + 1
            if a == "i":
                jiami_last = jiami_last + "ada"
                count = count + 1
            if a == "j":
                jiami_last = jiami_last + "adb"
                count = count + 1
            if a == "k":
                jiami_last = jiami_last + "adc"
                count = count + 1
            if a == "l":
                jiami_last = jiami_last + "add"
                count = count + 1
            if a == "m":
                jiami_last = jiami_last + "ade"
                count = count + 1
            if a == "n":
                jiami_last = jiami_last + "adf"
                count = count + 1
            if a == "o":
                jiami_last = jiami_last + "aea"
                count = count + 1
            if a == "p":
                jiami_last = jiami_last + "aeb"
                count = count + 1
            if a == "q":
                jiami_last = jiami_last + "aec"
                count = count + 1
            if a == "r":
                jiami_last = jiami_last + "aed"
                count = count + 1
            if a == "s":
                jiami_last = jiami_last + "aee"
                count = count + 1
            if a == "t":
                jiami_last = jiami_last + "aef"
                count = count + 1
            if a == "u":
                jiami_last = jiami_last + "afa"
                count = count + 1
            if a == "v":
                jiami_last = jiami_last + "afb"
                count = count + 1
            if a == "w":
                jiami_last = jiami_last + "afc"
                count = count + 1
            if a == "x":
                jiami_last = jiami_last + "afd"
                count = count + 1
            if a == "y":
                jiami_last = jiami_last + "afe"
                count = count + 1
            if a == "z":
                jiami_last = jiami_last + "aff"
                count = count + 1
            if a == "A":
                jiami_last = jiami_last + "baa"
                count = count + 1
            if a == "B":
                jiami_last = jiami_last + "bab"
                count = count + 1
            if a == "C":
                jiami_last = jiami_last + "bac"
                count = count + 1
            if a == "D":
                jiami_last = jiami_last + "bad"
                count = count + 1
            if a == "E":
                jiami_last = jiami_last + "bae"
                count = count + 1
            if a == "F":
                jiami_last = jiami_last + "baf"
                count = count + 1
            if a == "G":
                jiami_last = jiami_last + "bba"
                count = count + 1
            if a == "H":
                jiami_last = jiami_last + "bbb"
                count = count + 1
            if a == "I":
                jiami_last = jiami_last + "bbc"
                count = count + 1
            if a == "J":
                jiami_last = jiami_last + "bbd"
                count = count + 1
            if a == "K":
                jiami_last = jiami_last + "bbe"
                count = count + 1
            if a == "L":
                jiami_last = jiami_last + "bbf"
                count = count + 1
            if a == "M":
                jiami_last = jiami_last + "bca"
                count = count + 1
            if a == "N":
                jiami_last = jiami_last + "bcb"
                count = count + 1
            if a == "O":
                jiami_last = jiami_last + "bcc"
                count = count + 1
            if a == "P":
                jiami_last = jiami_last + "bcd"
                count = count + 1
            if a == "Q":
                jiami_last = jiami_last + "bce"
                count = count + 1
            if a == "R":
                jiami_last = jiami_last + "bcf"
                count = count + 1
            if a == "S":
                jiami_last = jiami_last + "bda"
                count = count + 1
            if a == "T":
                jiami_last = jiami_last + "bdb"
                count = count + 1
            if a == "U":
                jiami_last = jiami_last + "bdc"
                count = count + 1
            if a == "V":
                jiami_last = jiami_last + "bdd"
                count = count + 1
            if a == "W":
                jiami_last = jiami_last + "bce"
                count = count + 1
            if a == "X":
                jiami_last = jiami_last + "dbf"
                count = count + 1
            if a == "Y":
                jiami_last = jiami_last + "bea"
                count = count + 1
            if a == "Z":
                jiami_last = jiami_last + "beb"
                count = count + 1
            if a == "@":
                jiami_last = jiami_last + "bec"
                count = count + 1
            if a == " ":
                jiami_last = jiami_last + "bed"
                count = count + 1
            if a == "[":
                jiami_last = jiami_last + "bee"
                count = count + 1
            if a == "]":
                jiami_last = jiami_last + "bef"
                count = count + 1
            if a == ",":
                jiami_last = jiami_last + "bfa"
                count = count + 1
            if a == "{":
                jiami_last = jiami_last + "bfb"
                count = count + 1
            if a == "}":
                jiami_last = jiami_last + "bfc"
                count = count + 1
            if a == ":":
                jiami_last = jiami_last + "bfd"
                count = count + 1
            if a == "'":
                jiami_last = jiami_last + "bfe"
                count = count + 1
            if a == "\\":
                jiami_last = jiami_last + "bff"
                count = count + 1
        if count == 1:
            print(logs.日志("你没有输入任何内容", 色选="红色"))
            print(logs.日志("你输入了非法字符（除1-0，a-z，空格以外其他全是），请检查后重新开始，加密失败", 色选="红色"))
            exit()

        if counta == count:
            logs.系统日志("通过检查", PI)
            logs.系统日志(f"Fishconsole》passwordsys》count is {count}", PI)
            logs.系统日志(f"Fishconsole》passwordsys》counta is {counta}", PI)
        else:
            logs.系统日志(f"Fishconsole》passwordsys》count is {count}", PI)
            logs.系统日志(f"Fishconsole》passwordsys》counta is {counta}", PI)
            print(logs.颜色(logs.日志("你输入了非法字符（除1-0，a-z,空格以外其他全是），请检查后重新开始，加密失败"), 色选="红色"))
            exit()

        logs.系统日志("查看加密后的内容", PI)

        jiami_last = encrypt(jiami_last)
        logs.系统日志(f"Fishconsole》passwordsys》jiami_last is {jiami_last}", PI)
        logs.系统日志(f"加密成功", PI)
        return jiami_last
    else:
        # 解密

        logs.系统日志("验证密码", PI)
        password_res = [f"{id_protect}"] + [f"{password_a}"]
        logs.系统日志(f"Fishconsole》passwordsys》password_res is {password_res}", PI)
        if password_res is None:
            print(logs.颜色(logs.日志("用户取消了操作"), 色选="红色"))
            exit()
        p_res = ""
        t_res = ""
        for a in password_res[0]:
            p_res = p_res + a
        for a in password_res[1]:
            t_res = t_res + a
        jiemi_last = decrypt(t_res)

        logs.系统日志("查看解密加密的内容", PI)
        pattern = re.compile('.{3}')
        a = str(' '.join(pattern.findall(jiemi_last)))
        logs.系统日志(f"Fishconsole》passwordsys》pattern is {pattern}", PI)
        logs.系统日志(f"Fishconsole》passwordsys》a is {a}", PI)
        # 重新合并加密后的内容
        logs.系统日志("重新合并数据", PI)
        logs.系统日志("先将每个转化后的值进行拆分", PI)
        pattern_jiemi = (' '.join(pattern.findall(jiemi_last)))
        pattern_jiemi = pattern_jiemi.split(' ')
        pattern_resa = ""
        logs.系统日志(f"Fishconsole》passwordsys》pattern_jiemi is {pattern_jiemi}", PI)
        for a in pattern_jiemi:
            if a == "aaa":
                pattern_resa = pattern_resa + "1"
            if a == "aab":
                pattern_resa = pattern_resa + "2"
            if a == "aac":
                pattern_resa = pattern_resa + "3"
            if a == "aad":
                pattern_resa = pattern_resa + "4"
            if a == "aae":
                pattern_resa = pattern_resa + "5"
            if a == "aaf":
                pattern_resa = pattern_resa + "6"
            if a == "aba":
                pattern_resa = pattern_resa + "7"
            if a == "abb":
                pattern_resa = pattern_resa + "8"
            if a == "abc":
                pattern_resa = pattern_resa + "9"
            if a == "abd":
                pattern_resa = pattern_resa + "0"
            if a == "abe":
                pattern_resa = pattern_resa + "a"
            if a == "abf":
                pattern_resa = pattern_resa + "b"
            if a == "aca":
                pattern_resa = pattern_resa + "c"
            if a == "acb":
                pattern_resa = pattern_resa + "d"
            if a == "acc":
                pattern_resa = pattern_resa + "e"
            if a == "acd":
                pattern_resa = pattern_resa + "f"
            if a == "ace":
                pattern_resa = pattern_resa + "g"
            if a == "acf":
                pattern_resa = pattern_resa + "h"
            if a == "ada":
                pattern_resa = pattern_resa + "i"
            if a == "adb":
                pattern_resa = pattern_resa + "j"
            if a == "adc":
                pattern_resa = pattern_resa + "k"
            if a == "add":
                pattern_resa = pattern_resa + "l"
            if a == "ade":
                pattern_resa = pattern_resa + "m"
            if a == "adf":
                pattern_resa = pattern_resa + "n"
            if a == "aea":
                pattern_resa = pattern_resa + "o"
            if a == "aeb":
                pattern_resa = pattern_resa + "p"
            if a == "aec":
                pattern_resa = pattern_resa + "q"
            if a == "aed":
                pattern_resa = pattern_resa + "r"
            if a == "aee":
                pattern_resa = pattern_resa + "s"
            if a == "aef":
                pattern_resa = pattern_resa + "t"
            if a == "afa":
                pattern_resa = pattern_resa + "u"
            if a == "afb":
                pattern_resa = pattern_resa + "v"
            if a == "afc":
                pattern_resa = pattern_resa + "w"
            if a == "afd":
                pattern_resa = pattern_resa + "x"
            if a == "afe":
                pattern_resa = pattern_resa + "y"
            if a == "aff":
                pattern_resa = pattern_resa + "z"
            if a == "baa":
                pattern_resa = pattern_resa + "A"
            if a == "bab":
                pattern_resa = pattern_resa + "B"
            if a == "bac":
                pattern_resa = pattern_resa + "C"
            if a == "bad":
                pattern_resa = pattern_resa + "D"
            if a == "bae":
                pattern_resa = pattern_resa + "E"
            if a == "baf":
                pattern_resa = pattern_resa + "F"
            if a == "bba":
                pattern_resa = pattern_resa + "G"
            if a == "bbb":
                pattern_resa = pattern_resa + "H"
            if a == "bbc":
                pattern_resa = pattern_resa + "I"
            if a == "ddb":
                pattern_resa = pattern_resa + "J"
            if a == "bbe":
                pattern_resa = pattern_resa + "K"
            if a == "bbf":
                pattern_resa = pattern_resa + "L"
            if a == "bca":
                pattern_resa = pattern_resa + "M"
            if a == "bcb":
                pattern_resa = pattern_resa + "N"
            if a == "bcc":
                pattern_resa = pattern_resa + "O"
            if a == "bcd":
                pattern_resa = pattern_resa + "P"
            if a == "bce":
                pattern_resa = pattern_resa + "Q"
            if a == "bcf":
                pattern_resa = pattern_resa + "R"
            if a == "bda":
                pattern_resa = pattern_resa + "S"
            if a == "bdb":
                pattern_resa = pattern_resa + "T"
            if a == "bdc":
                pattern_resa = pattern_resa + "U"
            if a == "bdd":
                pattern_resa = pattern_resa + "V"
            if a == "bce":
                pattern_resa = pattern_resa + "W"
            if a == "bdf":
                pattern_resa = pattern_resa + "X"
            if a == "bea":
                pattern_resa = pattern_resa + "Y"
            if a == "beb":
                pattern_resa = pattern_resa + "Z"
            if a == "bed":
                pattern_resa = pattern_resa + " "
            if a == "bec":
                pattern_resa = pattern_resa + "@"
            if a == "bee":
                pattern_resa = pattern_resa + "["
            if a == "bef":
                pattern_resa = pattern_resa + "]"
            if a == "bfa":
                pattern_resa = pattern_resa + ","
            if a == "bfb":
                pattern_resa = pattern_resa + "{"
            if a == "bfc":
                pattern_resa = pattern_resa + "}"
            if a == "bfd":
                pattern_resa = pattern_resa + ":"
            if a == "bfe":
                pattern_resa = pattern_resa + "'"
            if a == "bff":
                pattern_resa = pattern_resa + "\\"

        logs.系统日志("读取加密信息", PI)
        text = pattern_resa.split("@", 1)[0]
        password = pattern_resa.split("@", 1)[1]
        logs.系统日志(f"Fishconsole》passwordsys》text is {text}", PI)
        logs.系统日志(f"Fishconsole》passwordsys》password is {password}", PI)
        if password == p_res:
            logs.系统日志("密码验证成功", PI)
            return f"{text}"
        else:
            print(logs.颜色(logs.日志("您的密码是错误的，请核对后重新输入"), 色选="红色"))
            exit()


def 密码(模式, 原文, 密码: str = ""):
    if 模式 == 1:
        a = 字符转unicode(1, 原文)
        logs.系统日志(f"a is {a}", PI)
        b = passwordsys(1, a, 密码)
        logs.系统日志(f"b is {b}", PI)
        return b
    elif not 模式:
        return 原文
    else:
        c = passwordsys(2, 密码, 原文)
        logs.系统日志(f"c is {c}", PI)
        d = 字符转unicode(2, c)
        logs.系统日志(f"d is {d}", PI)
        return d


# 模式,加密密码,内容
# a = password(1, 3, "1234567890")
# b = password(2, 3, a)


def 网易云音乐(歌单链接: list):
    import requests
    from lxml import html
    etree = html.etree

    urllist = 歌单链接
    base_url = 'https://link.hhtjim.com/163/'
    count = 0
    for url in urllist:
        count = count + 1
        print(logs.颜色(logs.分割线(f"开始第{count}次爬取", "Spider"), 色选="红色"))
        result = requests.get(url).text
        dom = etree.HTML(result)
        # //a[@contains内容(@href指定查找的内容,'song?'含有的)]/@href里面的链接文字
        ids = dom.xpath('//a[contains(@href,"song?")]/@href')
        names = dom.xpath('//a[contains(@href,"song?")]/text()')
        print(ids)
        a = -1
        for name in names:
            a = a + 1
            if not ('$' in name):
                if name != "{if x.album}":
                    if name != "{/if}":
                        count_id = ids[a].strip("/song?id=")
                        if not ('$' in count_id):
                            song_url = f"{base_url}{count_id}.mp3"
                            logs.系统日志(f'存储文件：{name}.mp3')
                            music = requests.get(song_url).content
                            with open(f'{name}.mp3', "wb") as file:
                                file.write(music)
                                file.close()


def 排名(数据源: list, 第几个: int):
    第几个 = 第几个 - 1
    a = 数据源
    for i in range(len(a)):
        for j in range(0, len(a) - 1):
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
    return a[第几个]


def 文件存在性检测(文件名: str):
    import os
    if not os.path.exists(文件名):
        logs.系统日志("文件存在性检测》文件未被发现，将返回布尔类型的值False", filecheck)
        file = False
    else:
        logs.系统日志("文件存在性检测》文件已被发现，将返回布尔类型的值Ture", filecheck)
        file = True
    return file


def 缓存(模式, 数据: dict = None, 文件名="Fishconsole.fcc"):
    模式 = str(模式)
    if 模式 == "1":
        数据 = str(数据)
        数据 = passwordsys(1, 数据, "")
        with open(f'{文件名}', "w") as file:
            file.write(数据)
            logs.系统日志("缓存》写入文件完成", cache)
            logs.系统日志(f"缓存》{文件名}", cache)
            file.close()
    elif 模式 == "2":
        if 文件存在性检测(f"{文件名}"):
            with open(f'{文件名}', "r") as file:
                a = file.read()
                file.close()
            解密 = passwordsys(2, "", a)
            解密 = eval(解密)
            解密 = dict(解密)
            logs.系统日志("缓存》读取文件完成", cache)
            logs.系统日志(f"缓存》{文件名}", cache)
            # 解密 = 解密.split(" ")
            return 解密
        else:
            # 如果它返回这个布尔值，那就说明它没有检测到这个文件
            logs.系统日志("缓存》文件存在性检测》指定文件并未发现，将返回布尔类型的False")
            return False
    else:
        logs.错误跟踪(["Fishconsole", "tool", "缓存"], "请使用合法的模式", 模式)


def 字符转unicode(模式, 原文: str):
    模式 = str(模式)
    原文 = str(原文)
    if 模式 == "1":
        原文 = 原文.encode('unicode_escape')
        logs.系统日志(f"》Fishconsole》字符串转unicode》type 原文 is {type(原文)}", ZUI)
        logs.系统日志(f"》Fishconsole》字符串转unicode》原文 is {原文}", ZUI)
        原文 = str(原文)
        logs.系统日志(f"》Fishconsole》字符串转unicode》type 原文 is {type(原文)}", ZUI)
        logs.系统日志(f"》Fishconsole》字符串转unicode》原文 is {原文}", ZUI)
        return 原文
    elif 模式 == "2":
        logs.系统日志(f"》Fishconsole》字符串转unicode》type 原文 is {type(原文)}", ZUI)
        logs.系统日志(f"》Fishconsole》字符串转unicode》原文 is {原文}", ZUI)
        b = 原文.replace("b'", "")
        c = b.replace("'", '')
        d = c.encode('utf-8').decode('unicode_escape')
        e = d.replace("nui", r"\u").encode('utf-8').decode('unicode_escape')
        logs.系统日志(f"》Fishconsole》字符串转unicode》type e is {type(e)}", ZUI)
        logs.系统日志(f"》Fishconsole》字符串转unicode》e is {e}", ZUI)
        return e


    else:
        logs.错误跟踪(["Fishconsole", "字符串转unicode", "模式"], "请选择正确的模式", {模式})


# 你要删我也没办法，反正如果出了什么错过了重大更新你就自己乐呵去呗

# 这个不是模块，我们将会在导入该模块的时候顺序执行此处
# sys是f_debug的强制更新的总开关，如果开启，更新器才会允许运行
sys = fcv.f_debug()
sys = sys["updata"]

UPI = fcv.f_debug()
UPI = UPI["updata"]

if sys:
    logs.系统日志("强制更新系统》强制更新系统启动", UPI)
    logs.系统日志("强制更新系统》读取缓存信息", UPI)
    config = 缓存(2)
    if not config:
        logs.系统日志("强制更新系统》缓存》缓存文件不存在，创建缓存文件", UPI)
        # fup的意思是tool模块判断自己是否在之前检测过一次，如果检测过一次，就是修改为正，让它可
        # +以在下一次检测到版本还是低的话继续保持未检测的状态，如果成功了，那就将False修改为ture，这个fupadta是独立的

        # 而updata是helps.帮助弄过来的，它的用处就是让tool执行强制更新的操作

        # 因为没有文件，所以我们在一开始就要创建文件，这个创建文件有一个规则，就是需要创建啥就写入啥，不要一股脑全写，因为这样就显得不高效
        config = {"updata": True, "fup": False}
        logs.系统日志("强制更新系统》首次运行，添加fup到缓存", UPI)
        # 提取数据，其实也是初始化首次启动时要用的变量
        fup = config["fup"]
        fupdata = config["updata"]
        # 当变量有点修改的时候我们就要进行保存，因为这样才能避免出现突如其来的故障
        缓存(1, config)
    else:
        # 当缓存文件存在时执行的操作
        logs.系统日志(f"缓存文件存在，尝试读取相关信息", UPI)
        logs.系统日志(f"Fishconsole.fcc is {config}", UPI)
        # 因为我们有文件了，我们就可以直接提取数据，但是难免会出现一些奇奇怪怪的情况，所以我们还要检测参数是否存在
        fup = config.get("fup")
        fupdata = config.get("updata")
        logs.系统日志(f"fup is {fup}", UPI)
        logs.系统日志(f"fupdata is {fupdata}", UPI)
        if fupdata is None:
            logs.系统日志("fupdata配置不存在，创建", UPI)
            config["updata"] = True
            缓存(1, config)
        if fup is None:
            logs.系统日志("fup配置不存在，创建", UPI)
            config["fup"] = True
            fup = config["fup"]
            缓存(1, config)

    # fupdata在前面的参数提取中就已经搞好了，现在我们只需要执行操作了
    if fupdata:
        logs.系统日志("这是updata值为True时执行的操作", UPI)
        if fup:
            print(logs.日志(f"》Fishconsole强制更新系统{fcv.version()}》tool 》您的版本过低，请更新至最新版本后重试", "红色"))
            # 最原始的操作，大家引以为戒
            # os.remove("Fishconsole.fcc")
            logs.系统日志(f"fup is {fup}", UPI)
            # 反转变量值，这样就可以在下一次执行的时候触发更新
            config["fup"] = False
            缓存(1, config)
            exit()
        else:
            # 这是tool的复检
            print(logs.日志(f"》Fishconsole强制更新系统{fcv.version()}》tool 》正在激活帮助及模块包更新检查工具", "红色"))
            # 反转变量值，这样就可以在下一次时触发警告
            config["fup"] = True
            # 只要缓存出现一次变化，我们就要把他存到fcc当中，只有这样我们才能保证它在异常关闭的时候数据不会丢失
            缓存(1, config)
            helps.帮助()
    else:
        logs.系统日志("这是updata值为False时执行的操作", UPI)
        config["fup"] = True
        缓存(1, config)
else:
    # 这是关闭了更新时执行的操作
    logs.日志("fcv_debug已取消强制更新系统的执行", "绿色")
