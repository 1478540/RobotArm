# 提供AI聊天的Chat模式
# 注意其中导入的TTS、BaiduAI、ASR_ARM、ConvertAudio、SoundPlay均是自己写的代码文件

import TTS
import speech_recognition as sr
import BaiduAI
import ASR_ARM
import ConvertAudio
import SoundPlay
import ARM
import re

# import ASR


global_is_set=False


#和AI进行持续的语音对话
#当说出指令"退出智能模式"则退出
def ChatWithAI_Baidu():

    global global_is_set
    global_is_set=True 
     
    # 初始化识别器
    r = sr.Recognizer()
    m = sr.Microphone(sample_rate=48000)

    r.dynamic_energy_threshold=False #关闭动态调整噪音环境，严格控制噪音水准
    r.energy_threshold=3000  #手动设置噪音阈值

    BaiduAI.initialize_AI()
    with m as s:
        print("请说话...")
        while True:
            audio=r.listen(s,phrase_time_limit=10)

            process_audio(audio)

            if not global_is_set:
                break
    
    return True



#处理音频的回调函数，返回值无实际意义，关键在于对全局变量global_is_set的设置
def process_audio(audio):
    global global_is_set

    try:
        # 转换为符合百度API要求的格式：PCM数据(推荐)、单声道、16000采样率、16位小端序
        audio_data = audio.get_raw_data(convert_rate=16000, convert_width=2)

#        text=ASR_ARM.process_data(audio_data)
        text=ASR_ARM.process_data(audio_data)

        if check_password(text):
            global_is_set=False
            return
        
        response=BaiduAI.ChatWithAI(text)
        parseAICommandText("temp.txt")
        #AI执行完命令后复位
        ARM.resetServoMove()
        print("AI指令执行完毕")

 
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))



def check_password(goal_str,password="退出智能模式"):
    if password in goal_str:
        return True
    else:
        return False


# # 解析AI回复的指令文本temp.txt
# # 将其转化为具体的命令执行
# def parseAICommandText(text_path="temp.txt"):
#     try:
#         # 读取文件内容
#         with open(text_path, 'r', encoding='utf-8') as file:
#             lines = file.readlines()
        
#         # 定义一个字典来映射函数名到实际函数
#         functions = {
#             "SpeechRespond": AIspeak,
#             "l2rServoMove": ARM.l2rServoMove,
#             "h2lServoMove": ARM.h2lServoMove,
#             "f2bServoMove": ARM.f2bServoMove,
#             "o2cServoMove": ARM.o2cServoMove
#         }
        
#         # 逐行检查并执行指令
#         for i in range(len(lines)):
#             line = lines[i].strip()  # 去除行首行尾的空格和换行符
#             if line.startswith("#函数调用") or line.startswith('# 函数调用'):
#                 # 检查下一行是否存在
#                 if i + 1 < len(lines):
#                     next_line = lines[i + 1].strip()
#                     # 正则表达式匹配函数调用
#                     function_call = re.search(r'(\w+)\((.*)\)', next_line)
#                     if function_call:
#                         func_name = function_call.group(1)
#                         params = function_call.group(2)
#                         # 解析参数
#                         param_dict = eval(f"dict({params})")
#                         # 调用相应的函数
#                         if func_name in functions:
#                             functions[func_name](**param_dict)
#                         else:
#                             print(f"未知的函数名: {func_name}")
#                     else:
#                         print(f"无法解析的函数调用: {next_line}")
#                 else:
#                     print(f"警告: `#函数调用`后没有跟随任何函数调用语句")
#     except Exception as e:
#         print(f"发生异常: {e}")

def parseAICommandText(text_path="temp.txt"):
    try:
        # 读取文件内容
        with open(text_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
        
        # 定义一个字典来映射函数名到实际函数
        functions = {
            "SpeechRespond": AIspeak,
            "l2rServoMove": ARM.l2rServoMove,
            "h2lServoMove": ARM.h2lServoMove,
            "f2bServoMove": ARM.f2bServoMove,
            "o2cServoMove": ARM.o2cServoMove
        }
        
        # 逐行检查并执行指令
        for line in lines:
            line = line.strip()  # 去除行首行尾的空格和换行符
            for func_name in functions:
                if line.startswith(func_name):
                    # 正则表达式匹配函数调用
                    function_call = re.search(r'(\w+)\((.*)\)', line)
                    if function_call:
                        params = function_call.group(2)
                        # 解析参数
                        param_dict = eval(f"dict({params})")
                        # 调用相应的函数
                        functions[func_name](**param_dict)
                    else:
                        print(f"无法解析的函数调用: {line}")
                    break  # 已找到函数调用并执行，跳出当前行的函数检查
    except Exception as e:
        print(f"发生异常: {e}")

#让AI说话的函数
#将参数字符串转化为音频，转格式，再通过扬声器播放
def AIspeak(text):
    TTS.synthesize_speech(text)
    ConvertAudio.convert_audio("audio.wav","new_audio.wav")
    SoundPlay.AudioPlay("new_audio.wav")



# def SpeechRespond(text):
#     print(f"SpeechRespond: {text}")

# def l2rServoMove(direction, angle, speed=0):
#     print(f"l2rServoMove: direction={direction}, angle={angle}, speed={speed}")

# def h2lServoMove(direction, angle, speed=0):
#     print(f"h2lServoMove: direction={direction}, angle={angle}, speed={speed}")

# def f2bServoMove(direction, angle, speed=0):
#     print(f"f2bServoMove: direction={direction}, angle={angle}, speed={speed}")

# def o2cServoMove(direction, angle, speed=0):
#     print(f"o2cServoMove: direction={direction}, angle={angle}, speed={speed}")



# ChatWithAI_Baidu()