#百度API客户端初始化程序

from aip import AipSpeech


# 百度语音应用(识别/合成共用) 的 APP_ID, API_KEY, SECRET_KEY
APP_ID = 'xxxxxxxxx'
API_KEY = 'xxxxxxxxxxxxxxxxxxxx'
SECRET_KEY = 'xxxxxxxxxxxxxxxxxxxxxxx'

# 初始化百度语音识别客户端
baidu_client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)


