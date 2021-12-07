# -*- coding = utf-8 -*-
# encoding: utf-8
# @Time : 2021.12.3 11:26
# @Author : Synthesis 杜品赫
# @File : graph.py
# @Software : PyCharm
# https://github.com/SynthesisDu/MC_BadAppleDGDH

import time
import matplotlib
from fchooser import *
from pylab import *
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import imageio


def create_gif(image_list, gif_name, duration=1.0):
    """
    :param image_list: 这个列表用于存放生成动图的图片
    :param gif_name: 字符串，所生成gif文件名，带.gif后缀
    :param duration: 图像间隔时间
    :return:
    """
    frames = []
    for image_name in image_list:
        frames.append(imageio.imread(image_name))

    imageio.mimsave(gif_name, frames, 'GIF', duration=duration)

def itemXY_2D_L(
        figSize_wid_len=(5, 4),
        dpi: int = 72,
        A_X: list = [1, 2, 2],
        A_Y: list = [3, 2, 2],
        B_X: list = [1, 2, 3],
        B_Y: list = [4, 5, 3],
        graph_title: str = "new graph",
        XLabel : str = "",
        YLabel : str = ""
):
    matplotlib.use('Agg')
    df = []
    # Dataset
    for i in range(len(A_X)):
        df.append(pd.DataFrame({'x_axis': [A_X[i], B_X[i]], 'y_axis': [A_Y[i], B_Y[i]]}))
    # plot
    fig = plt.figure(figsize=figSize_wid_len, dpi=dpi)
    for i in df:
        plt.plot('x_axis', 'y_axis', data=i, linestyle='-', marker='o')
    plt.title(graph_title)
    plt.xlabel(XLabel)
    plt.ylabel(YLabel)
    fig.savefig(graph_title.replace("/", "_") + '.png', dpi=dpi)

def itemXY_2D_XRankYRate(
        figSize_wid_len=(5, 4),
        dpi: int = 72,
        Y: list = [[1, 2, 2], [1, 2, 2], [1, 2, 2]],
        Y_lab : list = ["", "", ""],
        graph_title: str = "new graph",
        XLabel : str = "",
        YLabel : str = ""
):
    matplotlib.use('Agg')
    # plot
    fig = plt.figure(figsize=figSize_wid_len, dpi=dpi)
    X = np.arange(len(Y[0]))
    plt.bar(X + 0.00, Y[0], width=0.25, label=str(Y_lab[0]))
    plt.bar(X + 0.25, Y[1], width=0.25, label=str(Y_lab[1]))
    plt.bar(X + 0.50, Y[2], width=0.25, label=str(Y_lab[2]))
    plt.axhline(0, color='grey', linewidth=0.8)
    plt.legend()
    # W = [0.10, 0.25, 0.50]  # 偏移量
    # for i in range(3):
    #     for a, b in zip(X + W[i], Y[i]):  # zip拆包
    #         plt.text(a, b, "%.0f" % b, ha="center", va="bottom")  # 格式化字符串，保留0位小数
    plt.title(graph_title)
    plt.xlabel(XLabel)
    plt.ylabel(YLabel)
    fig.savefig(graph_title.replace("/", "_") + '.png', dpi=dpi)

def itemXYZ_3D_GIF(
        save_path : str,
        figSize_wid_len=(5, 4),
        dpi: int = 72,
        X: list = [1, 2, 3, 2, 1, 25, 32, 12, 1, 4, 3, 2, 10],
        Y: list = [5, 4, 3, 2, 10, 2, 3, 2, 1, 25, 32, 12, 1],
        Z: list = [10, 25, 32, 12, 1, 4, 3, 2, 10, 2, 3, 2, 1],
        graph_title: str = "new graph",
        x_name : str = "",
        y_name : str = "",
        z_name : str = "",
):
    matplotlib.use('Agg')
    os.mkdir(graph_title.replace("/", "_"))
    # Dataset
    df = pd.DataFrame({
        'X': X,
        'Y': Y,
        'Z': Z
    })
    count = 1
    name_list = []
    for rolling in range(360):
        save_name = "./" + graph_title.replace("/", "_") + "/" + str(rolling) + '.png'
        print("\rForming: " + str(count) + " / 360", end='')
        count += 1
        # plot
        fig = plt.figure(figsize=figSize_wid_len, dpi=dpi)
        ax = fig.add_subplot(111, projection='3d')
        ax.scatter(df['X'], df['Y'], df['Z'], c="black", s=100)
        ax.set_xlabel(x_name)
        ax.set_ylabel(y_name)
        ax.set_zlabel(z_name)
        ax.view_init(30, rolling)
        plt.title(graph_title)
        fig.savefig(save_name, dpi=dpi)
        name_list.append(save_name)
        plt.close(fig)
    if graph_title != "":
        gif = "./" + graph_title.replace("/", "_") + "/" + graph_title.replace("/", "_") + ".gif"
    else:
        gif = save_path + '/gif.gif'
    print("\n", end="")
    create_gif(name_list, gif, 0.01)


