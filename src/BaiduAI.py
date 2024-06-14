# 百度AI-千帆模型聊天程序
# 模型：ERNIT-lite-8k-0308


import requests
import json


#请在此处替换自己的 baiduAI(千帆模型) key
API_KEY = "xxxxxxxxxxxxxxxxxxxxx"
SECRET_KEY = "xxxxxxxxxxxxxxxxxxx"


# 全局变量，用于存储聊天上下文信息
Message = [
  {
    "role": "user",
    "content": "你好"
  },
  {
    "role": "assistant",
    "content": "\n```python\n#函数调用\nSpeechRespond(text=\"你好，我是机械臂智能助手，有什么我能帮你的吗？\")\n\n```\n"
  },
  {
    "role": "user",
    "content": "你能帮我做些什么事？"
  },
  {
    "role": "assistant",
    "content": "\n```python\n#函数调用\nSpeechRespond(text=\"我可以和你进行聊天，也可以根据你的需求操控机械臂行动\")\n\n```\n"
  },
  {
    "role": "user",
    "content": "你能展示一下操控机械臂的能力吗？"
  },
  {
    "role": "assistant",
    "content": "\n```python\n#函数调用\nSpeechRespond(text=\"当然，我会向上移动一下机械臂然后复原\")\n#函数调用\nh2lServoMove(direction=1,angle=30,speed=2)\n#函数调用\nh2lServoMove(direction=-1,angle=30,speed=2)\n\n```\n"
  },
  {
    "role": "user",
    "content": "你向右20度，向上10度有瓶可乐，你能帮我拿一下吗？"
  },
  {
    "role": "assistant",
    "content": "\n```python\n#函数调用\nSpeechRespond(text=\"当然，我会尝试向目标位置抓取可乐，并放到正中间\")\n#函数调用\nl2rServoMove(direction=-1,angle=20,speed=2)\n#函数调用\nh2lServoMove(direction=1,angle=10,speed=2)\n#函数调用\no2cServoMove(direction=1,angle=20,speed=2)\n#函数调用\no2cServoMove(direction=-1,angle=20,speed=2)\n\n```\n"
  },
  {
    "role": "user",
    "content": "你向左30度向下20度向前40度有个唇膏，你能帮我取一下吗？速度可以提快一点"
  },
  {
    "role": "assistant",
    "content": "\n```python\n#函数调用\nSpeechRespond(text=\"我已清楚指令，我会尝试抓取向左30度向下20度向前40度的唇膏，并且将速度等级从2提升到1\")\n#函数调用\nl2rServoMove(direction=1,angle=30,speed=1)\n#函数调用\nh2lServoMove(direction=-1,angle=20,speed=1)\n#函数调用\nf2bServoMove(direction=1,angle=40,speed=1)\n#函数调用\no2cServoMove(direction=1,angle=20,speed=1)\n#函数调用\no2cServoMove(direction=-1,angle=20,speed=1)\n\n```\n"
  },
  {
    "role": "user",
    "content": "你右前方有一个纸团，你能抓住它吗？这一次我希望你比上一次更快一点"
  },
  {
    "role": "assistant",
    "content": "\n```python\n#函数调用\nSpeechRespond(text=\"当然，虽然没有足够的角度信息，但我会尝试一下抓取纸团，并把速度提升到等级0\")\n#函数调用\nl2rServoMove(direction=-1,angle=30,speed=0)\n#函数调用\nf2bServoMove(direction=1,angle=30,speed=0)\n#函数调用\no2cServoMove(direction=1,angle=20,speed=0)\n#函数调用\no2cServoMove(direction=-1,angle=20,speed=0)\n\n```\n"
  },
  {
    "role": "user",
    "content": "你能操控机械臂模拟一下点头的动作吗？"
  },
  {
    "role": "assistant",
    "content": "\n```python\n#函数调用\nSpeechRespond(text=\"当然，我可以让机械臂小幅度地比较快地上下移动两下，这看上去就像是在点头\")\n#函数调用\nh2lServoMove(direction=-1,angle=20,speed=0)\n#函数调用\nh2lServoMove(direction=1,angle=20,speed=0)\n#函数调用\nh2lServoMove(direction=-1,angle=20,speed=0)\n#函数调用\nh2lServoMove(direction=1,angle=20,speed=0)\n\n```\n"
  },
]

SystemConfiguration=""

def get_access_token():
    """
    使用 AK，SK 生成鉴权签名（Access Token）
    :return: access_token，或是None(如果错误)
    """
    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {"grant_type": "client_credentials", "client_id": API_KEY, "client_secret": SECRET_KEY}
    return str(requests.post(url, params=params).json().get("access_token"))

def initialize_AI():
    global SystemConfiguration
    try:
        with open('BaiduAI_SystemConfiguration.txt', 'r', encoding='utf-8') as file:
            SystemConfiguration = file.read()
        print("SystemConfiguration initialized successfully.")
    except FileNotFoundError:
        print("Error: SystemConfiguration.txt file not found.")
    except Exception as e:
        print(f"An error occurred: {e}")



def add_message(role, content):
    # 添加消息到上下文
    global Message
    Message.append({
        "role": role,
        "content": content
    })


#ernie_speed ernie-lite-8k
def send_message_to_api():
    url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/ernie-lite-8k?access_token=" + get_access_token()
    
    payload = json.dumps({
        "messages": Message,
        "temperature": 0.20,
        "top_p": 0.7,
        "penalty_score": 1,
        "system": SystemConfiguration
    })
    headers = {
        'Content-Type': 'application/json'
    }
    
    response = requests.request("POST", url, headers=headers, data=payload)
    return response.json()


# AI聊天函数（具备上下文关联）
# question是问题字符串
# 返回AI的回复
def ChatWithAI(question):
    # 用户提问添加到上下文
    add_message("user", question)
    
    # 发送请求并获取响应
    response = send_message_to_api()
    
    # 从响应中提取assistant的回复并添加到上下文
    if 'result' in response:
        assistant_reply = response['result']
        add_message("assistant", assistant_reply)

        #将返回内容存储到.txt文件里
        save_string_to_file(assistant_reply)
        return assistant_reply
    else:
        return "Error: No result in response"



def save_string_to_file(string, filename='temp.txt'):
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(string)
        print(f"String successfully saved to {filename}.")
    except Exception as e:
        print(f"An error occurred while saving the string to file: {e}")


#if __name__ == '__main__':
#    # 示例调用
#    initialize_AI()
#
#
#    question=input("请输入你要问的问题\n")
#    result = ChatWithAI(question)

