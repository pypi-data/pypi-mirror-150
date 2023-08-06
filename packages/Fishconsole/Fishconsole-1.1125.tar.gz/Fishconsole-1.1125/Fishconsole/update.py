def update():
    from Fishconsole import fcv
    from Fishconsole import logs
    from Fishconsole import helps
    from Fishconsole import Fishsys

    # 你要删我也没办法，反正如果出了什么错过了重大更新你就自己乐呵去呗

    # 这个不是模块，我们将会在导入该模块的时候顺序执行此处
    # sys是f_debug的强制更新的总开关，如果开启，更新器才会允许运行
    sys = fcv.f_debug()
    sys = sys["updata"]

    UPI = fcv.f_debug()
    UPI = UPI["updata"]

    if sys:
        logs.系统日志("强制更新系统》强制更新系统启动", UPI)
        logs.系统日志("强制更新系统》读取Fishsys.缓存信息", UPI)
        config = Fishsys.缓存(2)
        if not config:
            logs.系统日志("强制更新系统》Fishsys.缓存》Fishsys.缓存文件不存在，创建Fishsys.缓存文件", UPI)
            # fup的意思是Fishsys模块判断自己是否在之前检测过一次，如果检测过一次，就是修改为正，让它可
            # +以在下一次检测到版本还是低的话继续保持未检测的状态，如果成功了，那就将False修改为ture，这个fupadta是独立的

            # 而updata是helps.帮助弄过来的，它的用处就是让Fishsys执行强制更新的操作
            # 因为没有文件，所以我们在一开始就要创建文件，这个创建文件有一个规则，就是需要创建啥就写入啥，不要一股脑全写，因为这样就显得不高效
            config = {"updata": True, "fup": False}
            logs.系统日志("强制更新系统》首次运行，添加fup到Fishsys.缓存", UPI)
            # 提取数据，其实也是初始化首次启动时要用的变量
            fup = config["fup"]
            fupdata = config["updata"]
            # 当变量有点修改的时候我们就要进行保存，因为这样才能避免出现突如其来的故障
            Fishsys.缓存(1, config)
        else:
            # 当Fishsys.缓存文件存在时执行的操作
            logs.系统日志(f"Fishsys.缓存文件存在，尝试读取相关信息", UPI)
            logs.系统日志(f"Fishconsole.fcc is {config}", UPI)
            # 因为我们有文件了，我们就可以直接提取数据，但是难免会出现一些奇奇怪怪的情况，所以我们还要检测参数是否存在
            fup = config.get("fup")
            fupdata = config.get("updata")
            logs.系统日志(f"fup is {fup}", UPI)
            logs.系统日志(f"fupdata is {fupdata}", UPI)
            if fupdata is None:
                logs.系统日志("fupdata配置不存在，创建", UPI)
                config["updata"] = True
                Fishsys.缓存(1, config)
            if fup is None:
                logs.系统日志("fup配置不存在，创建", UPI)
                config["fup"] = True
                fup = config["fup"]
                Fishsys.缓存(1, config)

        # fupdata在前面的参数提取中就已经搞好了，现在我们只需要执行操作了
        if fupdata:
            logs.系统日志("这是updata值为True时执行的操作", UPI)
            if fup:
                print(logs.日志(f"》Fishconsole强制更新系统{fcv.version()}》Fishsys 》您的版本过低，请更新至最新版本后重试", "红色"))
                # 最原始的操作，大家引以为戒
                # os.remove("Fishconsole.fcc")
                logs.系统日志(f"fup is {fup}", UPI)
                # 反转变量值，这样就可以在下一次执行的时候触发更新
                config["fup"] = False
                Fishsys.缓存(1, config)
                logs.安全退出("     <程序正常结束>")

            else:
                # 这是Fishsys的复检
                print(logs.日志(f"》Fishconsole强制更新系统{fcv.version()}》Fishsys 》正在激活帮助及模块包更新检查工具", "红色"))
                # 反转变量值，这样就可以在下一次时触发警告
                config["fup"] = True
                # 只要Fishsys.缓存出现一次变化，我们就要把他存到fcc当中，只有这样我们才能保证它在异常关闭的时候数据不会丢失
                Fishsys.缓存(1, config)
                helps.帮助()
        else:
            logs.系统日志("这是updata值为False时执行的操作", UPI)
            config["fup"] = True
            Fishsys.缓存(1, config)
    else:
        # 这是关闭了更新时执行的操作
        logs.日志("fcv_debug已取消强制更新系统的执行", "绿色")
