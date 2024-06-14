#机械臂的动作程序
#请注意！该程序对4台舵机的角度范围限制，以及函数detectionRange和函数convertAngle是根据实际安装的舵机角度编写的代码
#请根据安装时实际的舵机角度调试后修改代码，否则可能会影响4个机械臂的正常使用
# 机械臂的本质就是舵机的操作，并没有什么难度，麻烦的是舵机之间可能存在角度限制（而这需要根据实际情况来设定）

import SG90
import json
import time


#4台舵机的角度范围限制
BackAngleRestriction=160
FrontAngleRestriction=40

LeftAngleRestriction=170
RightAngleRestriction=0

OpenAngleRestriction=180
CloseAngleRestriction=160

HightAngleRestriction=160
LowAngleRestriction=0

#4台舵机的当前角度
l2rAngle = None
h2lAngle = None
f2bAngle = None
o2cAngle = None

#4台舵机的pwm信号
l2rServo=None
h2lServo=None
f2bServo=None
o2cServo=None

def init(signalPin0=21,signalPin1=20,signalPin2=16,signalPin3=12):
    initServo(signalPin0,signalPin1,signalPin2,signalPin3)
    initConfig()

def initServo(signalPin0,signalPin1,signalPin2,signalPin3):
    global l2rServo,h2lServo,f2bServo,o2cServo
    l2rServo=SG90.init(signalPin1)
    h2lServo=SG90.init(signalPin3)
    f2bServo=SG90.init(signalPin0)
    o2cServo=SG90.init(signalPin2)

#从文本ArmPosition.txt初始化舵机的4个当前角度到全局变量里
def initConfig(file_path='ArmPosition.txt'):
    global l2rAngle, h2lAngle, f2bAngle, o2cAngle

    # 打开文件并读取 JSON 数据
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    # 同步 JSON 数据到全局变量
    l2rAngle = data.get('l2rAngle')
    h2lAngle = data.get('h2lAngle')
    f2bAngle = data.get('f2bAngle')
    o2cAngle = data.get('o2cAngle')

def over():
    overServo()
    overConfig()

def overServo():
    global l2rAngle, h2lAngle, f2bAngle, o2cAngle
    SG90.over(l2rServo)
    SG90.over(h2lServo)
    SG90.over(f2bServo)
    SG90.over(o2cServo)

def overConfig(file_path='ArmPosition.txt'):
    global l2r, h2l, f2b, o2c

    # 创建一个字典保存全局变量的值
    data = {
        'l2rAngle': l2rAngle,
        'h2lAngle': h2lAngle,
        'f2bAngle': f2bAngle,
        'o2cAngle': o2cAngle
    }

    # 将字典写入文件
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4)



# 该函数控制机械臂前后移动
# direction=1则是向前移动，-1则是向后移动
# angle则是移动的角度
# is_rapid 决定是否快速移动
# speed 决定移动速度，取值有0~4一共4个等级，却小越快
def f2bServoMove(direction,angle,speed=0):
    global f2bServo,f2bAngle,FrontAngleRestriction,BackAngleRestriction
    try:
        assert direction == 1 or direction == -1
        assert f2bAngle!=None

        goal_angle=direction*angle+f2bAngle
        
        if goal_angle<FrontAngleRestriction: goal_angle=FrontAngleRestriction
        if goal_angle>BackAngleRestriction: goal_angle=BackAngleRestriction

        goal_angle=detectionRange(0,goal_angle)
        
        print(f2bAngle)
        print(goal_angle)

        if not speed:
            SG90.rapidly_servo_move(f2bServo,goal_angle)
        else:
            SG90.smooth_servo_move(f2bServo,f2bAngle,goal_angle,speed-1)

        f2bAngle=goal_angle
        
    except Exception as err:
        print(err)
        
    
# 该函数控制机械臂左右移动
# direction=1则是向左移动，-1则是向右移动
# angle则是移动的角度
# speed 决定移动速度，取值有0~4一共4个等级，却小越快
def l2rServoMove(direction,angle,speed=0):
    global l2rServo,l2rAngle,LeftAngleRestriction,RightAngleRestriction
    try:
        assert direction == 1 or direction == -1
        assert l2rAngle!=None

        goal_angle=direction*angle+l2rAngle
        
        if goal_angle>LeftAngleRestriction: goal_angle=LeftAngleRestriction
        if goal_angle<RightAngleRestriction: goal_angle=RightAngleRestriction

        print(l2rAngle)
        print(goal_angle)

        if not speed:
            SG90.rapidly_servo_move(l2rServo,goal_angle)
        else:
            SG90.smooth_servo_move(l2rServo,l2rAngle,goal_angle,speed-1)

        l2rAngle=goal_angle
        
    except Exception as err:
        print(err)


# 该函数控制机械臂张开闭合
# direction=1则是向打开，-1则是闭合
# angle则是移动的角度
# speed 决定移动速度，取值有0~4一共4个等级，却小越快
def o2cServoMove(direction,angle,speed=0):
    global o2cServo,o2cAngle,OpenAngleRestriction,CloseAngleRestriction
    try:
        assert direction == 1 or direction == -1
        assert o2cAngle!=None

        goal_angle=direction*angle+o2cAngle
        
        if goal_angle>OpenAngleRestriction: goal_angle=OpenAngleRestriction
        if goal_angle<CloseAngleRestriction: goal_angle=CloseAngleRestriction

        print(o2cAngle)
        print(goal_angle)

        if not speed:
            SG90.rapidly_servo_move(o2cServo,goal_angle)
        else:
            SG90.smooth_servo_move(o2cServo,o2cAngle,goal_angle,speed-1)

        o2cAngle=goal_angle
        
    except Exception as err:
        print(err)


######################   这段是关于有力夹子的废案   #############################
#夹子夹住时没有一点抓力，于是我开了一个子线程，让舵机超范围持续输出PWM信号，
#但是如果在子线程运行的同时运行其他舵机，子线程的PWM输出就会不稳定，舵机就会松手
#于是乎成了废案，这个机械臂只能表演表演节目


# def thread_function(event):
#     global o2cServo
#     print("夹子闭合")
#     o2cServo.ChangeDutyCycle(10.27)
#     # 等待事件被触发或超时100秒
#     event_is_set = event.wait(timeout=100)


#     if event_is_set:
#         print("夹子打开")

#     else:
#         print("夹子默认闭合时间已到，自动打开")

#     o2cServo.ChangeDutyCycle(12.5)
#     time.sleep(0.2)
#     o2cServo.ChangeDutyCycle(0)



# # 创建一个事件对象
# stop_event = threading.Event()
# # 线程列表
# ClawThreads=[]

# def openClaw():
#     try:
#         if len(ClawThreads)==1:
#             stop_event.set()
#             ClawThreads[0].join()
#             ClawThreads.pop()
#     except Exception as err:
#         print(err)

# def closeClaw():
#     global stop_event,ClawThreads

#     if len(ClawThreads)>0:
#         if ClawThreads[0].is_alive():
#             return 
#         else:
#             ClawThreads.pop()
    
#     try:
#         # 如果stop_event已经存在并触发了，需要清除状态以确保未触发
#         if stop_event.is_set():
#             stop_event.clear()
        
#         # 创建并启动子线程
#         thread = threading.Thread(target=thread_function, args=(stop_event,))
#         thread.start()
#         ClawThreads.append(thread)

#     except Exception as err:
#         print(err)
######################   这段是关于有力夹子的废案   #############################




# 该函数控制机械臂抬高降低
# direction=1则是抬高，-1则是降低
# angle则是移动的角度
# speed 决定移动速度，取值有0~4一共4个等级，却小越快
def h2lServoMove(direction,angle,speed=0):
    global h2lServo,h2lAngle,HightAngleRestriction,LowAngleRestriction
    try:
        assert direction == 1 or direction == -1
        assert h2lAngle!=None

        goal_angle=direction*angle+h2lAngle
        
        if goal_angle>HightAngleRestriction: goal_angle=HightAngleRestriction
        if goal_angle<LowAngleRestriction: goal_angle=LowAngleRestriction

        goal_angle=detectionRange(1,goal_angle)

        print(h2lAngle)
        print(goal_angle)
        
        if not speed:
            SG90.rapidly_servo_move(h2lServo,goal_angle)
        else:
            SG90.smooth_servo_move(h2lServo,h2lAngle,goal_angle,speed-1)

        h2lAngle=goal_angle
        
    except Exception as err:
        print(err)


#复位动作
def resetServoMove(speed=0):
    global h2lAngle,h2lServo
    global l2rAngle,l2rServo
    global o2cAngle,o2cServo
    global f2bAngle,f2bServo

    l2rResetAngle=85
    f2bResetAngle=80
    h2lResetAngle=160
    o2cResetAngle=160

    count=2
    while count: 
        count -= 1
        if l2rAngle-l2rResetAngle!=0:
            l2rServoMove((l2rResetAngle-l2rAngle)//abs(l2rAngle-l2rResetAngle),abs(l2rAngle-l2rResetAngle),speed)
            time.sleep(1)
        if f2bAngle-f2bResetAngle!=0:
            f2bServoMove((f2bResetAngle-f2bAngle)//abs(f2bAngle-f2bResetAngle),abs(f2bAngle-f2bResetAngle),speed)
            time.sleep(1)
        if h2lAngle-h2lResetAngle!=0:
            h2lServoMove((h2lResetAngle-h2lAngle)//abs(h2lAngle-h2lResetAngle),abs(h2lAngle-h2lResetAngle),speed)
            time.sleep(1)
        if o2cAngle-o2cResetAngle!=0:
            o2cServoMove((o2cResetAngle-o2cAngle)//abs(o2cAngle-o2cResetAngle),abs(o2cAngle-o2cResetAngle),speed)
            time.sleep(1)


# 表示赞同 的 点头动作
def nodServoMove(speed=0):
    resetServoMove()

    count=3
    while count:
        count -=1
        h2lServoMove(-1,15,speed)
        h2lServoMove(1,15,speed)


# 表示否认 的 摇头动作
def shakeheadServoMove(speed=0):
    resetServoMove()

    l2rServoMove(-1,15,speed)
    count=2
    while count:
        count -=1
        l2rServoMove(1,30,speed)
        l2rServoMove(-1,30,speed)
    
    l2rServoMove(1,30,speed)
    l2rServoMove(-1,15,speed)



# 机械臂左臂何右臂舵机转角之间有范围限制，会相互影响
# 以下规则是根据实际安装情况制定的，不同的安装情况会有不一样的限制
# 1.二者夹角不能超过150度
# 2.二者夹角不能小于40度
# 3.当左臂>150度时，右臂必须大于60度
# flag==1时代表左臂，其余代表右臂
def detectionRange(flag,goal_angle):
    global f2bAngle,h2lAngle

    limit_angle=0
    current_angle=0
    if flag:
        if f2bAngle<60:
            goal_angle=min(150,goal_angle)
        limit_angle=convertAngle(f2bAngle)
        current_angle=h2lAngle
       
    else:
        if h2lAngle>150:
            goal_angle=max(60,goal_angle)
        limit_angle=convertAngle(h2lAngle)
        current_angle=f2bAngle


    if goal_angle>current_angle>limit_angle:
        goal_angle=min(goal_angle,limit_angle+150)
    elif current_angle>goal_angle>limit_angle:
        goal_angle=max(goal_angle,limit_angle+40)
    elif current_angle>limit_angle>goal_angle:
        goal_angle=max(goal_angle,limit_angle+40)
    elif limit_angle>current_angle>goal_angle:
        goal_angle=max(goal_angle,limit_angle-150)
    elif limit_angle>goal_angle>current_angle:
        goal_angle=min(goal_angle,limit_angle-40)
    elif goal_angle>limit_angle>current_angle:
        goal_angle=min(goal_angle,limit_angle-40)
    

    return goal_angle

# 只用于左右臂之间的相对角度转化,工具函数
# 左臂的70度对齐于右臂的70度，二者反方向增长
def convertAngle(angle):
    return 140 - angle


##测试区
#
#GPIOpre.init()
#init()
#
#SG90.rapidly_servo_move(o2cServo,180)
#
#
#over()
#GPIOpre.over()