# ecoding=utf-8
import easygui
# 虽然没什么用，但是里面的强制更新系统可以很好的牵制调用
from Fishconsole import Fishsys
from Fishconsole import logs
logs.系统日志("用户调用了window模块")



def 弹窗(显示文字, 标题, 确认显示文字):
    显示文字 = str(显示文字)
    标题 = str(标题)
    确认显示文字 = str(确认显示文字)
    easygui.msgbox(显示文字, 标题, 确认显示文字)


def 选择对话框(显示文字, 标题, 选项: list, 图片地址: str = None):
    显示文字 = str(显示文字)
    标题 = str(标题)
    返回 = easygui.buttonbox(image=图片地址, msg=显示文字, title=标题, choices=选项)
    return 返回


def 列表选择对话框(显示文字, 标题, 选项: list):
    标题 = str(标题)
    返回 = easygui.multchoicebox(msg=显示文字, title=标题, choices=选项)
    return 返回


def 输入框(显示文字, 输入框标题, 标题=None):
    标题 = str(标题)
    显示文字 = str(显示文字)
    返回 = easygui.multenterbox(显示文字, title=标题, fields=输入框标题)
    return 返回


def 输入框a(显示文字, 输入框标题, 标题=None):
    标题 = str(标题)
    显示文字 = str(显示文字)
    返回 = easygui.multenterbox(显示文字, title=标题, fields=输入框标题)

    return 返回


def 密码框(显示文字, 输入框标题, 标题=None):
    标题 = str(标题)
    显示文字 = str(显示文字)
    返回 = easygui.multpasswordbox(显示文字, title=标题, fields=输入框标题)
    return 返回


def 文件选择():
    返回 = easygui.fileopenbox()
    return 返回


def 文件保存():
    返回 = easygui.filesavebox()
    return 返回
# 弹窗(1,2,3)
# print(选择对话框(1,2,选项=["ab","cd","ef"],图片地址="h.PNG"))
# print(列表选择对话框(1,2,选项=["ab","cd"]))
# print(输入框("显示文字",["内容1","内容2"],"标题"))
# print(密码框("显示文字",["内容1","内容2"],"标题"))
# print(文件选择())
# print(文件保存())

