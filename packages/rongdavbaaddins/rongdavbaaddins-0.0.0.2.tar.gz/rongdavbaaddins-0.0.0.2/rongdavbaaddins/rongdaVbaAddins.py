'''
Vba功能显示数量界面

'''
# -*- coding: utf-8 -*-
import os
import time
import traceback

try:
    from Ui.rongdaVbaAddinsUi import Ui_MainWindow
except:
    from .Ui.rongdaVbaAddinsUi import Ui_MainWindow
from PyQt5.QtWidgets import *
from PyQt5.QtCore import  *
from PyQt5 import QtCore, QtGui, QtWidgets
from clazz import demo
import json, datetime

import sys, hashlib
sys.path.insert(0 , os.path.dirname(os.path.abspath(__file__)))
import psutil
import shutil
style =  '''
    QPushButton#btn1 {
    height: 50px;
    background-color: qlineargradient(x1:1, y1:0, x2:1, y2:1, stop:0 #8a9195, stop: 1 balck);
    color: white;
    border-radius: 5px;
    font-size: 20px;
    font-weight:bold;
}

QPushButton#btn1:hover {
    background-color: qlineargradient(x1:1, y1:0, x2:1, y2:1, stop:0 #7d8488, stop: 1 balck);
}

QPushButton#btn1:pressed {
    background-color: qlineargradient(x1:1, y1:0, x2:1, y2:1, stop:0 #6a7073, stop: 1 balck);
}

QPushButton#btn2 {
    height: 50px;
    background-color: qlineargradient(x1:0, y1:0.5, x2:1, y2:0.5, stop:0 #47a7ed, stop: 1 #a967b2);
    color: white;
    border-radius: 25px;
    font-size: 20px;
    font-weight:bold;

}

QPushButton#btn2:hover {
    background-color: qlineargradient(x1:0, y1:0.5, x2:1, y2:0.5, stop:0 #459ee0, stop: 1 #995da1);
}

QPushButton#btn2:pressed {
    background-color: qlineargradient(x1:0, y1:0.5, x2:1, y2:0.5, stop:0 #4093d1, stop: 1 #87538e);
}
'''
import datetime
import requests
import random
class rongdaVbaAddinsUi(QMainWindow, Ui_MainWindow, demo.FunctionObject):

    numberSignal = pyqtSignal(int)
    warningSiganl = pyqtSignal(str)
    startTimeSignal = pyqtSignal()
    def __init__(self, communication=None, token = ""):
        super(rongdaVbaAddinsUi, self).__init__(communication)
        self.setupUi(self)
        self.setStyleSheet(style)
        self.FunctionName = "gonneng1"
        self.description = '''
=================================================
功能介绍：这是将rongdaVbaAddins
包名：rongdaVbaAddinsUi
版本号：0.1.1
作者：仇星， 王卫东
教程地址：https://alidocs.dingtalk.com/i/p/4oJRz0VRJyvmLZMydy0mV7WvjQn7MG89
=================================================
'''
        self.setWindowTitle( "rongdaVbaAddins")
        self.numberSignal.connect(self.updateNumberFun)
        self.startTimeSignal.connect(self.startTimeFun)

    def updateNumberFun(self, number):
        self.numEdit.setText(str(number))
        NowTime = datetime.datetime.now()
        self.nowTime.setText(NowTime.strftime('%Y-%m-%d %H:%M:%S'))
        self.nowTime_3.setText((NowTime + datetime.timedelta(seconds= 10)).strftime('%Y-%m-%d %H:%M:%S'))
        # self.nowTime_3.setText((NowTime + datetime.timedelta(minutes= 1)).strftime('%Y-%m-%d %H:%M:%S'))

    def QMessageBoxFun(self, word):
        QMessageBox.warning(self, "warning", word)

    def showEvent(self, a0: QtGui.QShowEvent):
        super(rongdaVbaAddinsUi, self).showEvent(a0)
        self.startTimeSignal.emit()

    def startTimeFun(self):
        print('这是输出当前文件所在位置')
        print(os.path.abspath(__file__))
        UUidFilePath = os.path.abspath(__file__)
        APPDATApath = os.getenv('APPDATA')
        AddinsPath = os.path.join(APPDATApath, 'Microsoft\AddIns')
        print("这是输出AddIns所在文件夹")
        print(AddinsPath)
        with open(os.path.join(AddinsPath, r'rongtoolspath.txt'), 'w', encoding="utf8") as f:
            f.write(UUidFilePath.split(r'\clazz\rongdaVbaAddins')[0])
        self.ifProcessRunning("wps.exe")
        self.ifProcessRunning('EXCEL.exe')

        uuidFileName = os.path.join(os.path.dirname(UUidFilePath), '荣大工具箱.xlam')
        AddInsFileName = os.path.join(AddinsPath, '荣大工具箱.xlam')

        LocalDirPath = os.getenv('APPDATA').replace('Roaming', 'Local')
        OfficePath = os.path.join(LocalDirPath, 'Microsoft\Office')
        uuidExcelPath = os.path.join(os.path.dirname(UUidFilePath), 'Excel.officeUI')
        AddInsExcelPath = os.path.join(OfficePath, 'Excel.officeUI')
        if os.path.isfile(uuidFileName):
            if os.path.isfile(AddInsFileName):
                hash1 = self.get_file_hash(uuidFileName)
                hash2 = self.get_file_hash(AddInsFileName)
                if hash1 != hash2:
                    print('荣大工具箱.xlam 文件hash不一样')
                    try:
                        shutil.copy(uuidFileName, AddInsFileName)
                    except:
                        traceback.print_exc()
                else:
                    print('荣大工具箱.xlam 文件内容一样跳过移动')
            else:
                print('addIns文件中不存在 荣大工具箱.xlam 文件')
                try:
                    shutil.copy(uuidFileName, AddInsFileName)
                except:
                    traceback.print_exc()
        print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
        if os.path.isfile(uuidExcelPath):
            if os.path.isfile(AddInsExcelPath):
                hash1 = self.get_file_hash(uuidExcelPath)
                hash2 = self.get_file_hash(AddInsExcelPath)
                if hash1 != hash2:
                    print('Excel.officeUI 文件hash不一样')
                    try:
                        shutil.copy(uuidExcelPath, AddInsExcelPath)
                    except:
                        traceback.print_exc()
                else:
                    print('Excel.officeUI文件内容一样跳过移动')
            else:
                print('addIns文件中不存在 Excel.officeUI 文件')
                try:
                    shutil.copy(uuidExcelPath, AddInsExcelPath)
                except:
                    traceback.print_exc()


        self.UpdateThread = UpdateNum(self)
        self.UpdateThread.start()

    def get_file_hash( self ,file_path):
        with open(file_path, 'rb') as f:
            file_hash = hashlib.sha256()
            while chunk := f.read(8192):
                file_hash.update(chunk)
        return file_hash.hexdigest()

    def hideEvent(self, a0: QtGui.QHideEvent) -> None:
        print('这是隐藏事件')
        super(rongdaVbaAddinsUi, self).hideEvent(a0)
        self.UpdateThread.terminate()

    def ifProcessRunning(self,process_name):
        self.closeSet = set()
        for proc in psutil.process_iter():
            try:
                if process_name.lower() in proc.name().lower() and process_name.lower() not in self.closeSet:
                    buttonReply = QMessageBox.question(None, '选择提示框', f"{process_name}正在执行！您是否要强制关闭？", QMessageBox.Yes | QMessageBox.No,
                                                       QMessageBox.No)
                    if buttonReply == QMessageBox.Yes:
                        print('你选择了 Yes')
                        # print(f'taskkill /f /im {process_name}')
                        output = os.popen(f'taskkill /f /im {process_name}')
                        print(output.read())

                    else:
                        print('你选择了 No')
                    self.closeSet.add(process_name.lower())
            except Exception as e:
                traceback.print_exc()
                QMessageBox.warning(self, 'warning', f'关闭{process_name}失败！失败原因为{str(e)}。建议您手动关闭')
        return False

#更新数量的类
class UpdateNum(QThread):
    def __init__(self,communication):
        super(UpdateNum, self).__init__()
        self.communication = communication
    def run(self):
        while True:
            CanUseNum = self.GetFunNum('vbarongdatools001', self.communication.token)
            print(CanUseNum)
            if CanUseNum:
                self.communication.numberSignal.emit(CanUseNum)
            else:
                self.communication.numberSignal.emit(0)
            time.sleep(10)

    def GetFunNum(self, functionName,token):
        # url = f'http://127.0.0.1:9000/vadmin/auth/GetFuncitonNum'
        url = f'http://39.102.142.236:19518/vadmin/auth/GetFuncitonNum'
        headers = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Authorization": f"bearer {token}",
            'Connection': 'keep-alive',
            'Cookie': 'jenkins-timestamper-offset=-28800000',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36 SE 2.X MetaSr 1.0"

        }
        data = {
            "function": functionName
        }
        response = requests.post(url, headers=headers, params=data)
        print(response.text)
        if response.status_code != 200:
            num = 0
            while num < 3:
                time.sleep(random.uniform(0.5, 1))
                response = requests.post(url=url, headers=headers)
                if response.status_code == 200:
                    if response.json()["code"] == 200:
                        #返回数量

                        return response.json()['data']
                if num == 2:
                    print(  f"响应状态码为：{response.status_code},报错原因为：{response.text}")
                    return False
                num += 1
        elif response.status_code == 200:
            if response.json()["code"] == 200:
                return  response.json()['data']
            else:
                print( f"响应状态码为：{response.json()['code']},报错原因为：{response.json()['message']}")
                return False
        else:
            print( f"响应状态码为：{response.status_code},报错原因为：{response.text}")
            return False

if __name__ == '__main__':

    app = QApplication(sys.argv)
    myWin = rongdaVbaAddinsUi()
    myWin.show()
    sys.exit(app.exec_())