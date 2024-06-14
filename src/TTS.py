# 语音合成程序
# 调用了百度语音合成SDK，所以需要配合BaiduClient.py使用


from BaiduClient import baidu_client

tts_client=baidu_client



# 语音合成
# text为要合成的目标文本
# 会生成audio.wav音频文件
def synthesize_speech(text):
    global tts_client
    
    result = tts_client.synthesis(text, 'zh', 1, {
        'vol': 9,  #音量
        'per': 4,  #角色
        'pit': 4,  #音调
    })
    
    # 识别正确返回语音二进制，错误则返回dict 参照下面错误码
    if not isinstance(result, dict):
        with open('audio.wav', 'wb') as f:
            f.write(result)

