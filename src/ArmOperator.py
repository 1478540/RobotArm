#机械臂命令操作程序
#主要负责 指令 以及 机械臂 动作 之间的映射关系

import ASR_ARM
import MatrixKeyBoard
import ARM
import re
import sys
import AIChatMode



def init():
    ARM.init()
    MatrixKeyBoard.init()


def over():
    ARM.over()



#操作模式
#可以取值0、1、2、3  分别对应着左右、前后、高低、开合的操作
operator_mode=0

def VoiceOperation():
    ASR_ARM.Trigger_ASR_BaiduApi()
    # result=ASR_ARM.SHORT_ASR_BaiduApi(5,5)
    # print(result[0])
    # check_password(result[0],password_commands)


def AddAngleOperation(angle,speed=0):
    if operator_mode==0:
        command_left(angle,speed)
    elif operator_mode==1:
        command_forward(angle,speed)
    elif operator_mode==2:
        command_up(angle,speed)
    else:
        command_open(angle,speed)

    
def ReduceAngleOperation(angle,speed=0):
    if operator_mode==0:
        command_right(angle,speed)
    elif operator_mode==1:
        command_back(angle,speed)
    elif operator_mode==2:
        command_down(angle,speed)
    else:
        command_close(angle,speed)


NORMAL_SIGNAL = 1323
OVER_SIGNAL = 1324
QUIT_SIGNAL = 1325

def command_left(angle=0,speed=2):
    global NORMAL_SIGNAL
    ARM.l2rServoMove(1,angle,speed)
    return NORMAL_SIGNAL

def command_right(angle=0,speed=2):
    global NORMAL_SIGNAL
    ARM.l2rServoMove(-1,angle,speed)
    return NORMAL_SIGNAL

def command_up(angle=0,speed=2):
    global NORMAL_SIGNAL
    ARM.h2lServoMove(1,angle,speed)
    return NORMAL_SIGNAL

def command_down(angle=0,speed=2):
    global NORMAL_SIGNAL
    ARM.h2lServoMove(-1,angle,speed)
    return NORMAL_SIGNAL

def command_forward(angle=0,speed=2):
    global NORMAL_SIGNAL
    ARM.f2bServoMove(1,angle,speed)
    return NORMAL_SIGNAL

def command_back(angle=0,speed=2):
    global NORMAL_SIGNAL
    ARM.f2bServoMove(-1,angle,speed)
    return NORMAL_SIGNAL

def command_open(angle=0,speed=2):
    global NORMAL_SIGNAL
    ARM.o2cServoMove(1,angle,speed)
    return NORMAL_SIGNAL

def command_close(angle=0,speed=2):
    global NORMAL_SIGNAL
    ARM.o2cServoMove(-1,angle,speed)
    return NORMAL_SIGNAL

#参数angle没有任何意义，只是为了参数对齐
def command_quit(angle=0,speed=2):
    global QUIT_SIGNAL
    print("退出语音模式")
    return QUIT_SIGNAL

#参数angle没有任何意义，只是为了参数对齐
def command_over(angle=0,speed=2):
    global OVER_SIGNAL
    print("程序结束")
    sys.exit()
    return OVER_SIGNAL

#参数angle没有任何意义，只是为了参数对齐
def command_reset(angle=0,speed=2):
    global NORMAL_SIGNAL
    ARM.resetServoMove()
    print("机械臂已复位")
    return NORMAL_SIGNAL

#参数angle没有任何意义，只是为了参数对齐
def command_nod(angle=0,speed=2):
    global NORMAL_SIGNAL
    ARM.nodServoMove()
    print("对对对")
    return NORMAL_SIGNAL

#参数angle没有任何意义，只是为了参数对齐
def command_shakehead(angle=0,speed=2):
    global NORMAL_SIGNAL
    ARM.shakeheadServoMove()
    print("错错错")
    return NORMAL_SIGNAL

#参数angle没有任何意义，只是为了参数对齐
def command_AIChat(angle=0,speed=2):
    global NORMAL_SIGNAL

    print("进入AI聊天模式")
    AIChatMode.ChatWithAI_Baidu()
    print("已退出AI聊天模式")

    return NORMAL_SIGNAL

# 定义命令列表及其对应的执行函数
password_commands = [
    ("左转", command_left),
    ("向左", command_left),
    ("右转", command_right),
    ("向右", command_right),
    ("上抬", command_up),
    ("抬起", command_up),
    ("向上", command_up),
    ("上台", command_up),
    ("下压", command_down),
    ("向下", command_down),
    ("前进", command_forward),
    ("向前", command_forward),
    ("后退", command_back),
    ("向后", command_back),
    ("张开", command_open),
    ("打开", command_open),
    ("关闭", command_close),
    ("闭合", command_close),
    ("退出语音模式", command_quit),
    ("程序结束",command_over),
    ("复位",command_reset),
    ("点头",command_nod),
    ("摇头",command_shakehead),
    ("进入智能模式",command_AIChat)
]

def check_password(goal_str, password=password_commands):
    for cmd_str, cmd_func in password:
        if cmd_str in goal_str:
            angle=extract_first_number(goal_str)
            if angle!=None:
                return cmd_func(angle)
            else:
                return cmd_func()
        

def extract_first_number(goal_str):
    # 使用正则表达式提取第一个数字
    match = re.search(r'\d+', goal_str)
    if match:
        return int(match.group())
    else:
        return None
