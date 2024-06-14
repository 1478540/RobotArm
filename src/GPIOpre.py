# GPIO配置文件，负责初始化以及清理GPIO引脚资源

import RPi.GPIO as GPIO

def init():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)

def over():
	GPIO.cleanup()