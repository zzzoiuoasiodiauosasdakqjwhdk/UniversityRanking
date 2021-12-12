# -*- coding = utf-8 -*-
# encoding: utf-8
# @Time : 2021.12.10 19:14
# @Author : https://github.com/SynFUN / https://github.com/SynthesisDu
# @File : data2graph.py
# @Software : PyCharm

from pathfinder import *
from pylab import *
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import imageio


dictionary = {
        "name": 0,
        "fee": 1,
        "location": 2
}


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


def Axis2PNG_DisparityGraph(cur, x_name, y_name, titleT):
    for i in cur.execute("PRAGMA table_info('unv')").fetchall():
        dictionary.update({i[1]: int(i[0])})
        dictionary.update({i[0]: int(i[0])})
    cur.execute("select * from unv;")
    ax, ay, by = [], [], []
    for i in cur.fetchall():
        if i[dictionary[x_name]] is not None and i[dictionary[y_name]] is not None:
            if i[dictionary[x_name]] != 'NoneType' and i[dictionary[y_name]] != 'NoneType':
                ay.append(float(i[dictionary[x_name]]))
                by.append(float(i[dictionary[y_name]]))
    matplotlib.use('Agg')
    df = []
    # Dataset
    for i in range(len(by)):
        df.append(pd.DataFrame({'x_axis': [by[i], ay[i]], 'y_axis': [ay[i], by[i]]}))
    # plot
    fig = plt.figure(figsize=(10, 10), dpi=100)
    for i in df:
        plt.plot('x_axis', 'y_axis', data=i, linestyle='-', marker='o')
    plt.title(titleT)
    path = fileSaver(
        title="Save Image File",
        filetypes=[('PNG file', '*.png')],
        defaultextension=".png",
        initialfile=titleT.replace("/", "_")
    )
    fig.savefig(path, dpi=100)


def Axis3PNG_CompareGraph(cur, a, b, c, names, titleT):
    for i in cur.execute("PRAGMA table_info('unv')").fetchall():
        dictionary.update({i[1]: int(i[0])})
        dictionary.update({i[0]: int(i[0])})
    cur.execute("select * from unv;")
    r1, r2, r3 = [], [], []
    for i in cur.fetchall():
        if i[dictionary[a]] is not None and i[dictionary[b]] is not None and i[dictionary[c]] is not None:
            if i[dictionary[a]] != 'NoneType' and i[dictionary[b]] != 'NoneType' and i[dictionary[c]] != 'NoneType':
                if i[dictionary[a]] != 0 and i[dictionary[b]] != 0 and i[dictionary[c]] != 0:
                    r1.append(float(i[dictionary[a]]))
                    r2.append(float(i[dictionary[b]]))
                    r3.append(float(i[dictionary[c]]))
    matplotlib.use('Agg')
    # plot
    fig = plt.figure(figsize=(10, 10), dpi=100)
    X = np.arange(len(r1))
    plt.bar(X + 0.00, r1, width=0.25, label=str(names[0]))
    plt.bar(X + 0.25, r2, width=0.25, label=str(names[1]))
    plt.bar(X + 0.50, r3, width=0.25, label=str(names[2]))
    plt.axhline(0, color='grey', linewidth=0.8)
    plt.legend()
    plt.title(titleT)
    path = fileSaver(
        title="Save Image File",
        filetypes=[('PNG file', '*.png')],
        defaultextension=".png",
        initialfile=titleT.replace("/", "_")
    )
    fig.savefig(path, dpi=100)

def Axis3GIF_DisparityGraph(cur, x_name, y_name, z_name, names, titleT):
    for i in cur.execute("PRAGMA table_info('unv')").fetchall():
        dictionary.update({i[1]: int(i[0])})
        dictionary.update({i[0]: int(i[0])})
    cur.execute("select * from unv;")
    X, Y, Z = [], [], []
    for i in cur.fetchall():
        if i[dictionary[x_name]] is not None and i[dictionary[y_name]] is not None and i[dictionary[z_name]] is not None:
            if i[dictionary[x_name]] != 'NoneType' and i[dictionary[y_name]] != 'NoneType' and i[dictionary[z_name]] != 'NoneType':
                if i[dictionary[x_name]] != 0 and i[dictionary[y_name]] != 0 and i[dictionary[z_name]] != 0:
                    X.append(float(i[dictionary[x_name]]))
                    Y.append(float(i[dictionary[y_name]]))
                    Z.append(float(i[dictionary[z_name]]))
    matplotlib.use('Agg')
    os.mkdir(titleT.replace("/", "_"))
    # Dataset
    df = pd.DataFrame({
        'X': X,
        'Y': Y,
        'Z': Z
    })
    count = 1
    name_list = []
    path = folderChooser("Choose A Folder To Save GIF And Frame Section")
    for rolling in range(360):
        save_name = path + "/" + str(rolling) + '.png'
        print("\rForming: " + str(count) + " / 360", end='')
        count += 1
        # plot
        fig = plt.figure(figsize=(10, 10), dpi=100)
        ax = fig.add_subplot(111, projection='3d')
        ax.scatter(df['X'], df['Y'], df['Z'], c="black", s=100)
        ax.set_xlabel(names[0])
        ax.set_ylabel(names[1])
        ax.set_zlabel(names[2])
        ax.view_init(30, rolling)
        plt.title(titleT)
        fig.savefig(save_name, dpi=100)
        name_list.append(save_name)
        plt.close(fig)
    if titleT != "":
        gif = path + "/" + titleT.replace("/", "_") + ".gif"
    else:
        gif = path + '/gif.gif'
    print("\n", end="")
    create_gif(name_list, gif, 0.01)


def expect(cur, rate1, rank, titleT, rate2=-1):
    if rate2 == -1:
        for i in cur.execute("PRAGMA table_info('unv')").fetchall():
            dictionary.update({i[1]: int(i[0])})
            dictionary.update({i[0]: int(i[0])})
            dictionary.update({int(i[0]): int(i[0])})
        cur.execute("select * from unv;")
        p1, pm = [], []
        pSum = 0.0
        count = 1
        for i in cur.fetchall():
            if i[dictionary[rate1]] is not None and i[dictionary[rank]] is not None:
                if i[dictionary[rate1]] != 'NoneType' and i[dictionary[rank]] != 'NoneType':
                    p1.append(float(i[dictionary[rate1]]))
                    pSum += float(i[dictionary[rate1]]) * float(i[dictionary[rank]])
                    count += 1
        print(str(titleT) + " is : " + str(pSum))
    else:
        for i in cur.execute("PRAGMA table_info('unv')").fetchall():
            dictionary.update({i[1]: int(i[0])})
            dictionary.update({i[0]: int(i[0])})
        cur.execute("select * from unv;")
        p1, p2, pm = [], [], []
        pSum = 0.0
        count = 1
        for i in cur.fetchall():
            if i[dictionary[rate1]] is not None and i[dictionary[rate2]] is not None and i[dictionary[rank]] is not None:
                if i[dictionary[rate1]] != 'NoneType' and i[dictionary[rate2]] != 'NoneType' and i[dictionary[rank]] != 'NoneType':
                    p1.append(float(i[dictionary[rate1]]))
                    p2.append(float(i[dictionary[rate2]]))
                    pSum += float(i[dictionary[rate1]]) * float(i[dictionary[rate2]]) * float(i[dictionary[rank]])
                    count += 1
        print(str(titleT) + " is : " + str(pSum))
