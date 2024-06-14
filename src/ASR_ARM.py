# 调用百度API实现语音识别程序(机械臂程序专用版)
# 请配合BaiduClient.py使用

import speech_recognition as sr
import ArmOperator
from BaiduClient import baidu_client




#录音一句话并识别，请确保插入麦克风
# total_time: 录音最长时常
# delay_time: 最长允许延迟时常(开始录音delay_time后若没有声音则结束)
def SHORT_ASR_BaiduApi(total_time,delay_time):
    
    # 初始化识别器
    r = sr.Recognizer()

    # 从默认麦克风获取数据
    with sr.Microphone(sample_rate=48000) as source:
        print("请说话...")
        audio = r.listen(source, timeout=delay_time, phrase_time_limit=total_time)

    # 转换为符合百度API要求的格式：PCM数据(推荐)、单声道、16000采样率、16位小端序
    audio_data = audio.get_raw_data(convert_rate=16000, convert_width=2)

    # 使用百度语音识别
    try:
        print("百度语音识别结果：")
        result = baidu_client.asr(audio_data, 'pcm', 16000, {'dev_pid': 1537})

        # 输出识别结果
        if result['err_no'] == 0:
            return result['result']
        else:
            print("百度语音识别错误信息：", result['err_msg'])
    except sr.UnknownValueError:
        print("无法理解音频")
    except sr.RequestError as e:
        print("服务请求错误; {0}".format(e))



global_is_set=True               #用于Trigger_ASR_BaiduApi函数全局变量,判断Trrigger_ASR_BaiduApi是否应该退出


#在一段对话中等待口令，直到识别口令才返回True
def Trigger_ASR_BaiduApi():
    global global_is_set
    global_is_set=True 
     
    # 初始化识别器
    r = sr.Recognizer()
    m = sr.Microphone(sample_rate=48000)

    r.dynamic_energy_threshold=False #关闭动态调整噪音环境，严格控制噪音水准
    r.energy_threshold=3000  #手动设置噪音阈值

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

        text=process_data(audio_data)

        if ArmOperator.check_password(text) == ArmOperator.QUIT_SIGNAL:
            global_is_set=False
 
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))


#使用百度API，返回语音识别的字符串
def process_data(data):

    # 使用百度语音识别
    try:
        print("百度语音识别结果：")
        result = baidu_client.asr(data, 'pcm', 16000, {'dev_pid': 1537})

        # 判断识别结果
        if result['err_no'] == 0:
            text=result['result']
            print(text[0])
            return text[0]
        
    except Exception as e:
        print(f"处理音频时出错: {e}")


