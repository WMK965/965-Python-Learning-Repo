from PyQt5 import QtCore, QtGui, uic
from PyQt5.QtWidgets import *
import tkinter as tk
from tkinter import filedialog
import jieba
import wordcloud
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

root = tk.Tk()
root.withdraw()


class mainthread:

    def __init__(self):
        self.mainWindow = uic.loadUi('main.ui')
        self.mainWindow.FileChooseButton.clicked.connect(self.Choose_File)
        self.mainWindow.MaskChooseButton.clicked.connect(self.Choose_Mask)
        #self.mainWindow.GenerateButton.actions(self.Generate_Action())

    #文本选择
    def Choose_File(self):
        global file_path, cursor
        file_path = "./resources/111.txt"
        file_path = filedialog.askopenfilename()
        self.mainWindow.FilePathPreview.setText(file_path)
        cursor = self.mainWindow.LogBrowser.textCursor()
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertText(f"[Sys]:File path selected:{file_path}\n")
        self.mainWindow.LogBrowser.setTextCursor(cursor)
        self.mainWindow.LogBrowser.ensureCursorVisible()

    #蒙版选择
    def Choose_Mask(self):
        global mask_path
        mask_path = "./resources/mask.png"
        mask_path = filedialog.askopenfilename()
        self.mainWindow.MaskPathPreview.setText(mask_path)
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertText(f"[Sys]:Mask path selected:{mask_path}\n")
        self.mainWindow.LogBrowser.setTextCursor(cursor)
        self.mainWindow.LogBrowser.ensureCursorVisible()

    @staticmethod
    def Generate_Action():
        raw_data = open(file_path).read()
        ls = jieba.lcut(raw_data)
        text = ' '.join(ls)
        open(file_path).close()
        mask = np.array(Image.open(mask_path))
        wc = wordcloud.WordCloud(font_path="msyh.ttc",
                                 mask=mask,
                                 background_color='white',
                                 max_font_size=240,
                                 stopwords={'王勃', '一'})
        wc.generate(text)
        wc.to_file("./results/111.png")
        plt.imshow(wc)
        plt.axis("off")
        plt.show()


global file_path
global mask_path


if __name__ == '__main__':
    app = QApplication([])

    # 显示UI

    m_main = mainthread()
    m_main.mainWindow.show()

    app.exec_()
