#SG90舵机利用pwm原理工作
#红线(中间)连接5V电压，棕/黑线连接GND，橙色线连接信号引脚


import RPi.GPIO as GPIO
import time


#舵机初始化，并返回舵机操作的PWM信号
def init(signal_pin):
    GPIO.setup(signal_pin, GPIO.OUT, initial=False)
    p = GPIO.PWM(signal_pin, 50)  # 频率50Hz，周期20ms
    p.start(0)
#    time.sleep(0.1)  # 增加延迟，确保PWM信号和舵机初始化完成
    return p

#结束舵机的PWM信号操作
def over(p):
    p.stop()


#该函数 控制 舵机 从0度转到目标角度，再从目标角度回到0度，来回摆动固定次数
# signal_pin: 控制信号引脚BCM编号
# angle: 来回偏转角度（0~180）
# delay: 延迟时间(秒)
# times：来回摆动次数
def SwingFunction(p, angle, delay, times):

    while times > 0:
        times -= 1

        # 从0度转到目标角度
        smooth_servo_move(p, 0, angle)
        time.sleep(delay)

        # 从目标角度转回到0度
        smooth_servo_move(p, angle, 0)
        time.sleep(delay)
    
    p.ChangeDutyCycle(0)



# 该函数 实现 舵机平滑转动舵机
# p为pwm信号,start_angle为开始角度，end_engle为结束角度
# speed 决定速度，依次是0，1，2，3 其中1是最稳定的工作速度，数字越小速度越快
def smooth_servo_move(p, start_angle, end_angle,speed=1):
    if start_angle==end_angle:return
    
    #这四个速度是根据实际情况调试得到的
    speeds=[(1,0.01),(1,0.02),(2,0.08),(1,0.08)]
    
    # step决定每次转动的角度差，delay决定每次转动的延迟（由二者共同决定转动的平滑程度）
    step=speeds[speed][0]
    delay=speeds[speed][1]
 
    if start_angle < end_angle:
        angle_range = range(start_angle, end_angle, step)
    else:
        angle_range = range(start_angle, end_angle, -step)

    set_servo_angle(p, start_angle)  # 确保最终达到初始角度
    time.sleep(0.2)
    
    for angle in angle_range:
        set_servo_angle(p, angle)
        time.sleep(delay)

    set_servo_angle(p, end_angle)  # 确保最终达到目标角度
    time.sleep(0.2)

    p.ChangeDutyCycle(0)
    


# 该函数 实现 舵机快速转动到指定角度
# p为pwm信号,end_engle为结束角度
def rapidly_servo_move(p,end_angle):
    
    set_servo_angle(p, end_angle)  
    time.sleep(0.2)
    p.ChangeDutyCycle(0)

# 工具函数：控制舵机转动到指定角度
def set_servo_angle(p, angle):
    duty_cycle = angle_to_duty_cycle(angle)
    p.ChangeDutyCycle(duty_cycle)


# 工具函数：计算角度对应的占空比
def angle_to_duty_cycle(angle):
    return angle / 18 + 2.5




##测试区
#
#GPIO.setmode(GPIO.BCM)
#GPIO.setwarnings(False)
#
#
#servo=init(12)
#
##rapidly_servo_move(servo,80)
#smooth_servo_move(servo,140,160)
## 暂停 PWM 输出，确保舵机保持固定位置
#servo.ChangeDutyCycle(0)
##SwingFunction(servo, 180, 0.1, 2)
#print('工作完毕')
#
#over(servo)
#GPIO.cleanup()

