import os
import sys
from io import BytesIO

from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication

from ai_module import ali_nls
from core import wsa_server
from gui import flask_server
from gui.window import MainWindow
from utils import config_util
from scheduler.thread_manager import MyThread
import plugin.vtube_studio as vtube_studio


def __clear_samples():
    if not os.path.exists("./samples"):
        os.mkdir("./samples")
    for file_name in os.listdir('./samples'):
        if file_name.startswith('sample-') and file_name.endswith('.mp3'):
            os.remove('./samples/' + file_name)


def __clear_songs():
    if not os.path.exists("./songs"):
        os.mkdir("./songs")
    for file_name in os.listdir('./songs'):
        if file_name.endswith('.mp3'):
            os.remove('./songs/' + file_name)




if __name__ == '__main__':
    __clear_samples()
    __clear_songs()
    config_util.load_config()

    # 连接 ue4 人物模型
    ws_server = wsa_server.new_instance(port=10002)
    ws_server.start_server()

    # 获取
    web_ws_server = wsa_server.new_web_instance(port=10003)
    web_ws_server.start_server()

    # 连接VtubeStudio
    ws_vts_client = vtube_studio.new_instance(host="127.0.0.1", port=18001)
    ws_vts_client.start_client()


    ali_nls.start()
    flask_server.start()
    app = QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon('icon.png'))
    win = MainWindow()
    win.show()
    app.exit(app.exec_())

    
