import librosa
import time
import pygame
import numpy as np
import uuid
from core.wsa_client import MyClient
from utils import util

# 调用vtubeStudioApi 控制人物模型


# vts ws
__web_vts_instance: MyClient = None

requestId: str = None
authenticationToken: str = None
pluginName: str = "fay vts"
pluginDeveloper: str = "ajc"

class VtuberStudioClient(MyClient):
    def __init__(self, host='0.0.0.0', port=10000):
        super().__init__(host, port)
    
    def on_connect_handler(self):
        check_authority()

def new_instance(host='0.0.0.0', port=10000) -> MyClient:
    global __web_vts_instance
    if __web_vts_instance is None:
        __web_vts_instance = VtuberStudioClient(host, port)
    return __web_vts_instance

def get_instance() -> MyClient:
    return __web_vts_instance

def play_audio(audio_path):
    pygame.mixer.init()
    pygame.mixer.music.load(audio_path)  
    pygame.mixer.music.set_volume(0.8) 

    x , sr = librosa.load(audio_path, sr=8000)

    x = x  - min(x)
    x = x  / max(x)
    x= np.log(x) + 1
    x = x  / max(x) * 1.2

    pygame.mixer.music.play()
    s_time = time.time()
    try:
        for _ in range(int(len(x) / 800)):
            it = x[int((time.time() - s_time) * 8000)+1]
            # print(it)
            if it < 0:
                it = 0
            # 发送数据到vts
            say({"id": "MouthOpen","value": it})
            time.sleep(0.1)
    except:
        pass

    time.sleep(0.1)
    # 发送数据到vts
    say({"id": "MouthOpen","value": 0})

# ws连接上后第一步：检查vts插件授权
def check_authority():
    requestId = str(uuid.uuid1())
    message = __web_vts_instance.send_cmd({
        "apiName": "VTubeStudioPublicAPI",
        "apiVersion": "1.0",
        "requestID": requestId,
        "messageType": "APIStateRequest"
    })
    # 判断data是否成功
    util.log(message)
    
# 登录vts 获取token
def long():
    message = __web_vts_instance.send_cmd({
        "apiName": "VTubeStudioPublicAPI",
        "apiVersion": "1.0",
        "requestID": requestId,
        "messageType": "AuthenticationTokenRequest",
        "data": {
            "pluginName": pluginName,
            "pluginDeveloper": pluginDeveloper
        }
    })

# 修改vts 参数
def say(data):
    message = __web_vts_instance.send_cmd({
        "apiName": "VTubeStudioPublicAPI",
        "apiVersion": "1.0",
        "requestID": requestId,
        "messageType": "InjectParameterDataRequest",
        "data": {
            "parameterValues": [
                data
            ]
        }
    })

