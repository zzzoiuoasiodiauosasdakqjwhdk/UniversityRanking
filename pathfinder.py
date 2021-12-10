# -*- coding = utf-8 -*-
# encoding: utf-8
# @Time : 2021.11.18 09:04
# @Author : https://github.com/SynFUN / https://github.com/SynthesisDu
# @File : pathfinder.py
# @Software : PyCharm

from tkinter import filedialog
import tkinter

def folderChooser(title: str) -> str:
    """
    :param title: 窗口名称 The name of the folder chooser window
    :return: 选取的文件夹的路径 The selected folder's path
    """
    tkinter.Tk().withdraw()
    path = tkinter.filedialog.askdirectory(title=title)
    return path


def fileChooser(title: str, filetypes: list = None) -> str:
    """
    :param title: 窗口名称 The name of the folder chooser window
    :param filetypes: [('File Type Describe', '*.filename_extension'), ('TXT File', '*.txt'), ('Audio File', '*.mp3')]
    :return: 选取的文件的路径 The selected file's path
    """
    tkinter.Tk().withdraw()
    if filetypes is None:
        filetypes = [('All Files', '*')]
    path = tkinter.filedialog.askopenfilename(title=title, filetypes=filetypes)
    return path


def fileSaver(title: str, filetypes: list, defaultextension: str, initialfile: str) -> str:
    """
    :param title: 窗口名称 The name of the folder chooser window
    :param filetypes: [('File Type Describe', '*.filename_extension'), ('TXT File', '*.txt'), ('Audio File', '*.mp3')]
    :param defaultextension: 补全扩展名 Default file extension
    :param initialfile: 补全文件名 Default file name
    :return: 保存的文件的路径 The saved file's path
    """
    tkinter.Tk().withdraw()
    path = tkinter.filedialog.asksaveasfilename(title=title, filetypes=filetypes, defaultextension=defaultextension,
                                                initialfile=initialfile)
    return path
