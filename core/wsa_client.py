from asyncio import AbstractEventLoop

import websockets
from websockets import client
import asyncio
import json
from abc import abstractmethod

from scheduler.thread_manager import MyThread
from utils import util

class MyClient:
    def __init__(self, host='0.0.0.0', port=10000):
        self.__host = host  # ip
        self.__port = port  # 端口号
        self.__client = None
        self.__event_loop: AbstractEventLoop = None
        self.__running = True
        self.__pending = None
        self.isConnect = False

    def __del__(self):
        self.stop_client()
    
    # 往要发送的命令列表中，添加命令
    async def __myconnect(self):
        self.__event_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.__event_loop)
        server_url = "ws://" + self.__host + ":" + str(self.__port)
        util.log(1,"开始连接:{}".format(server_url))
        try:
             async with client.connect(server_url) as websocket:
                util.log(1,"websocket连接上:{}".format(self.__port))
                self.__client = websocket
                # 连接成功回调
                self.isConnect = True
                self.on_connect_handler()
        except ConnectionRefusedError as e:
            # 服务端未启动，或连接失败时退出.
            print("e:", e)
            return
        
    #Edit by coderajc on 20230705:通过继承此类来实现客户端端的连接处理逻辑
    @abstractmethod
    def on_connect_handler(self):
        pass
    
        
    # 往要发送的命令列表中，添加命令
    async def send_cmd(self, content):
        # 发送数据并打印服务端返回结果
        await self.__client.send(content)
        recv_text = await self.__client.recv()
        return recv_text
        
    # 开启服务
    def start_client(self):
        self.__myconnect()
        # MyThread(target=self.__myconnect).start()
        
    # 关闭client
    def stop_client(self):
        self.__running = False
        self.isConnect = False
        self.__client = None
        self.__client.close(reason="exit")