import wordcloud
from PyQt5 import QtGui, uic
from PyQt5.QtWidgets import *
import tkinter as tk
from tkinter import filedialog, messagebox
import WcModule
import sys
import chardet

root = tk.Tk()
root.withdraw()
WcModule.size = 210
WcModule.maxword = 75
WcModule.font = "msyh.ttc"
WcModule.stopwords = {'1', '2'}


# noinspection PyGlobalUndefined
class mainthread:

    def __init__(self):
        global boot1
        global boot2
        global boot3
        boot1 = 0
        boot2 = 0
        boot3 = 0
        #程序初始化模块功能
        self.mainWindow = uic.loadUi('main.ui')
        self.mainWindow.FileChooseButton.clicked.connect(self.Choose_File)
        self.mainWindow.MaskChooseButton.clicked.connect(self.Choose_Mask)
        self.mainWindow.StopWordEdit.setEchoMode(QLineEdit.Normal)
        self.mainWindow.StopWordEdit.textChanged.connect(self.textChanged)
        self.mainWindow.StopWordApplyButton.clicked.connect(self.Confirm_input)
        self.mainWindow.FontSelectBox.addItems(['微软雅黑 R', '华文行楷 R', '楷体 R', 'Adobe 黑体 Std R', '宋体 R', '幼圆 R'])
        self.mainWindow.FontSelectBox.currentIndexChanged.connect(self.selectionChange)
        self.mainWindow.FontSizeSelectBox.valueChanged.connect(self.valueChange1)
        self.mainWindow.MaxWordCountBox.valueChanged.connect(self.valueChange2)
        self.mainWindow.GenerateButton.clicked.connect(lambda: self.Generate_Action())

    # 文本选择
    def Choose_File(self):
        file_path = filedialog.askopenfilename()
        WcModule.file = file_path
        cursor = self.mainWindow.LogBrowser.textCursor()
        global boot1
        #检测是否选中文件
        if file_path == "":
            boot1 = 0
            self.mainWindow.FilePathPreview.setText(file_path)
            cursor.movePosition(QtGui.QTextCursor.End)
            cursor.insertText(f"[Sys]:File path unselected\n")
            self.mainWindow.LogBrowser.setTextCursor(cursor)
            self.mainWindow.LogBrowser.ensureCursorVisible()
            self.alert_box("输入路径为空")
        else:
            self.mainWindow.FilePathPreview.setText(file_path)
            data = open(file=file_path, mode='rb')
            result = chardet.detect(data.read())
            result = result["encoding"]
            cursor.movePosition(QtGui.QTextCursor.End)
            cursor.insertText(f"[Sys]:File path selected: {file_path}\n")
            self.mainWindow.LogBrowser.setTextCursor(cursor)
            self.mainWindow.LogBrowser.ensureCursorVisible()
            #文件编码识别
            if "GB" in result:
                boot1 = 1
                WcModule.codec = "gbk"
                cursor.movePosition(QtGui.QTextCursor.End)
                cursor.insertText(f"[Sys]:File codec detected: GB2312(GBK)\n")
                self.mainWindow.LogBrowser.setTextCursor(cursor)
                self.mainWindow.LogBrowser.ensureCursorVisible()
            elif "utf" in result:
                boot1 = 1
                WcModule.codec = "utf-8"
                cursor.movePosition(QtGui.QTextCursor.End)
                cursor.insertText(f"[Sys]:File codec detected: UTF-8\n")
                self.mainWindow.LogBrowser.setTextCursor(cursor)
                self.mainWindow.LogBrowser.ensureCursorVisible()
            elif "Johab" in result:
                boot1 = 1
                WcModule.codec = "johab"
                cursor.movePosition(QtGui.QTextCursor.End)
                cursor.insertText(f"[Sys]:File codec detected: Johab\n")
                WcModule.stopwords = {'of', 'to', 'the', 'on', 'and', 'in'}
                self.mainWindow.LogBrowser.setTextCursor(cursor)
                self.mainWindow.LogBrowser.ensureCursorVisible()
            elif "ascii" in result:
                boot1 = 1
                WcModule.codec = "ascii"
                cursor.movePosition(QtGui.QTextCursor.End)
                cursor.insertText(f"[Sys]:File codec detected: ASCII\n")
                WcModule.stopwords = {'of', 'to', 'the', 'on', 'and', 'in'}
                self.mainWindow.LogBrowser.setTextCursor(cursor)
                self.mainWindow.LogBrowser.ensureCursorVisible()
            else:
                boot1 = 0
                cursor.movePosition(QtGui.QTextCursor.End)
                cursor.insertText(f"[Sys]:File codec detection Failed\n")
                self.mainWindow.LogBrowser.setTextCursor(cursor)
                self.mainWindow.LogBrowser.ensureCursorVisible()

    # 蒙版选择
    def Choose_Mask(self):
        mask_path = filedialog.askopenfilename()
        WcModule.mask = mask_path
        cursor = self.mainWindow.LogBrowser.textCursor()
        global boot2
        boot2 = 0
        # 检测是否选中文件
        if mask_path == "":
            self.mainWindow.MaskPathPreview.setText(mask_path)
            cursor.movePosition(QtGui.QTextCursor.End)
            cursor.insertText(f"[Sys]:Mask path unselected\n")
            self.mainWindow.LogBrowser.setTextCursor(cursor)
            self.mainWindow.LogBrowser.ensureCursorVisible()
            self.alert_box("输入路径为空")
            boot2 = 0
        else:
            boot2 = 1
            self.mainWindow.MaskPathPreview.setText(mask_path)
            cursor.movePosition(QtGui.QTextCursor.End)
            cursor.insertText(f"[Sys]:Mask path selected: {mask_path}\n")
            self.mainWindow.LogBrowser.setTextCursor(cursor)
            self.mainWindow.LogBrowser.ensureCursorVisible()

    def valueChange1(self):
        font_size = 10 * self.mainWindow.FontSizeSelectBox.value()
        WcModule.size = font_size

    def valueChange2(self):
        max_word = self.mainWindow.MaxWordCountBox.value()
        WcModule.maxword = max_word

    def Confirm_input(self):
        cursor = self.mainWindow.LogBrowser.textCursor()
        # 检测是否有输入内容
        if boot3 == 0:
            cursor.movePosition(QtGui.QTextCursor.End)
            cursor.insertText(f"[Sys]:Stop words undefined\n")
            self.mainWindow.LogBrowser.setTextCursor(cursor)
            self.mainWindow.LogBrowser.ensureCursorVisible()
            self.alert_box("无输入")
        else:
            inp = str(input_words)
            inp = inp.replace('，', ',')
            inp = inp.split(',')
            WcModule.stopwords = set(inp)
            cursor.movePosition(QtGui.QTextCursor.End)
            cursor.insertText(f"[Sys]:Stop words: {set(inp)}\n")
            self.mainWindow.LogBrowser.setTextCursor(cursor)
            self.mainWindow.LogBrowser.ensureCursorVisible()

    @staticmethod
    def textChanged(text):
        global input_words
        global boot3
        boot3 = 1
        input_words = None
        input_words = text

    @staticmethod
    def selectionChange(i):
        WcModule.font = fontlist[i]

    @staticmethod
    def alert_box(str1):
        a = messagebox.showerror('Error', str1)
        print(a)

    def Generate_Action(self):
        cursor = self.mainWindow.LogBrowser.textCursor()
        # 检测参数完整与否
        if boot1 + boot2 == 2:
            cursor.movePosition(QtGui.QTextCursor.End)
            cursor.insertText(
                f"[Sys]:Parameters: {WcModule.size, WcModule.maxword, WcModule.font, WcModule.file, WcModule.mask, WcModule.stopwords, WcModule.codec}\n")
            cursor.insertText(f"[Sys]:Generating.....\n")
            self.mainWindow.LogBrowser.setTextCursor(cursor)
            self.mainWindow.LogBrowser.ensureCursorVisible()
            WcModule.generate(WcModule.size, WcModule.maxword, WcModule.font, WcModule.file, WcModule.mask, WcModule.stopwords, WcModule.codec)
        else:
            cursor.movePosition(QtGui.QTextCursor.End)
            cursor.insertText(f"[Sys]:Parameter missing\n")
            self.mainWindow.LogBrowser.setTextCursor(cursor)
            self.mainWindow.LogBrowser.ensureCursorVisible()
            self.alert_box("缺少必要参数")


#fontlist = ("./resources/msyh.ttc", "./resources/STXINGKA.TTF", "./resources/simkai.ttf", "./resources/AdobeHeitiStd-Regular.otf", "./resources/simsun.ttc", "./resources/SIMYOU.TTF")
fontlist = ("msyh.ttc", "STXINGKA.TTF", "simkai.ttf", "AdobeHeitiStd-Regular.otf", "simsun.ttc", "SIMYOU.TTF")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    m_main = mainthread()
    m_main.mainWindow.show()
    app.exec_()
