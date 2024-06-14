#矩阵键盘操控程序
#引脚 R1~R4 以及 C1~C4 的连接请符合全局变量的配置（目前该文件只连接了矩阵键盘的第一列按钮）


import RPi.GPIO as GPIO
import time

# 定义引脚
R1_PIN = 22  
R2_PIN = 27  
R3_PIN = 17  
R4_PIN = 4  

C1_PIN = 18  


# 矩阵键盘初始化
def init():

    # 设置引脚模式
    GPIO.setup(R1_PIN, GPIO.OUT)
    GPIO.setup(R2_PIN, GPIO.OUT)
    GPIO.setup(R3_PIN, GPIO.OUT)
    GPIO.setup(R4_PIN, GPIO.OUT)
    GPIO.setup(C1_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    # 初始化所有行引脚为高电平
    GPIO.output(R1_PIN, GPIO.HIGH)
    GPIO.output(R2_PIN, GPIO.HIGH)
    GPIO.output(R3_PIN, GPIO.HIGH)
    GPIO.output(R4_PIN, GPIO.HIGH)


# 检测矩阵按钮是否被按下
# 传入参数为按钮的相应引脚
# 如果按下则输出True,反之输出False
def check_button(row_pin, col_pin):   
    # 拉低行引脚
    GPIO.output(row_pin, GPIO.LOW)
    
    # 检查列引脚状态
    if GPIO.input(col_pin) == GPIO.LOW:
        GPIO.output(row_pin,GPIO.HIGH)
        return True
    else:
        GPIO.output(row_pin,GPIO.HIGH)
        return False