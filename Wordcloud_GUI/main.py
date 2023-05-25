from PyQt5 import QtGui, uic
from PyQt5.QtWidgets import *
import tkinter as tk
from tkinter import filedialog
import WcModule
import sys

root = tk.Tk()
root.withdraw()
WcModule.size = 210
WcModule.maxword = 75
WcModule.font = "AdobeHeitiStd-Regular.otf"
WcModule.file = "../resources/111.txt"
WcModule.mask = "../resources/mask.png"
WcModule.stopwords = {'王勃', '一'}


class mainthread:

    def __init__(self):
        self.mainWindow = uic.loadUi('main.ui')
        self.mainWindow.FileChooseButton.clicked.connect(self.Choose_File)
        self.mainWindow.MaskChooseButton.clicked.connect(self.Choose_Mask)
        self.mainWindow.StopWordEdit.setEchoMode(QLineEdit.Normal)
        self.mainWindow.StopWordEdit.textChanged.connect(self.textChanged)
        self.mainWindow.StopWordApplyButton.clicked.connect(self.Confirm_input)
        self.mainWindow.FontSelectBox.addItems(['Adobe 黑体 Std R', '华文行楷 R', '楷体 R', '微软雅黑 R', '宋体 R', '幼圆 R'])
        self.mainWindow.FontSelectBox.currentIndexChanged.connect(self.selectionChange)
        self.mainWindow.FontSizeSelectBox.valueChanged.connect(self.valueChange1)
        self.mainWindow.MaxWordCountBox.valueChanged.connect(self.valueChange2)
        self.mainWindow.GenerateButton.clicked.connect(lambda: self.Generate_Action())

    # 文本选择
    def Choose_File(self):
        file_path = filedialog.askopenfilename()
        WcModule.file = file_path
        self.mainWindow.FilePathPreview.setText(file_path)
        cursor = self.mainWindow.LogBrowser.textCursor()
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertText(f"[Sys]:File path selected:{file_path}\n")
        self.mainWindow.LogBrowser.setTextCursor(cursor)
        self.mainWindow.LogBrowser.ensureCursorVisible()

    # 蒙版选择
    def Choose_Mask(self):
        mask_path = filedialog.askopenfilename()
        WcModule.mask = mask_path
        cursor = self.mainWindow.LogBrowser.textCursor()
        self.mainWindow.MaskPathPreview.setText(mask_path)
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertText(f"[Sys]:Mask path selected:{mask_path}\n")
        self.mainWindow.LogBrowser.setTextCursor(cursor)
        self.mainWindow.LogBrowser.ensureCursorVisible()

    def valueChange1(self):
        font_size = 10 * self.mainWindow.FontSizeSelectBox.value()
        WcModule.size = font_size

    def valueChange2(self):
        max_word = self.mainWindow.MaxWordCountBox.value()
        WcModule.maxword = max_word

    @staticmethod
    def Confirm_input():
        inp = str(input_words)
        inp = inp.replace('，', ',')
        inp = inp.split(',')
        WcModule.stopwords = set(inp)

    @staticmethod
    def textChanged(text):
        global input_words
        input_words = text

    @staticmethod
    def selectionChange(i):
        WcModule.font = fontlist[i]

    def Generate_Action(self):
        cursor = self.mainWindow.LogBrowser.textCursor()
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertText(f"[Sys]:Parameters:{WcModule.size, WcModule.maxword, WcModule.font, WcModule.file, WcModule.mask, WcModule.stopwords}\n")
        cursor.insertText(f"[Sys]:Generating.....\n")
        self.mainWindow.LogBrowser.setTextCursor(cursor)
        self.mainWindow.LogBrowser.ensureCursorVisible()
        WcModule.generate(WcModule.size, WcModule.maxword, WcModule.font, WcModule.file, WcModule.mask, WcModule.stopwords)


fontlist = ("AdobeHeitiStd-Regular.otf", "STXINGKA.TTF", "simkai.ttf", "msyh.ttc", "simsun.ttc", "SIMYOU.TTF")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    m_main = mainthread()
    m_main.mainWindow.show()
    app.exec_()
