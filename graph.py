# -*- coding = utf-8 -*-
# encoding: utf-8
# @Time : 2021.12.3 11:26
# @Author : Synthesis 杜品赫
# @File : graph.py
# @Software : PyCharm
# https://github.com/SynthesisDu/MC_BadAppleDGDH

import time
import numpy as np
import matplotlib
import pandas as pd
import matplotlib.pyplot as plt
from fchooser import *
from pylab import *

matplotlib.use('Agg')


def quartile1_itemY_valueX(
        figSize_wid_len=(5, 4),
        dpi: int = 72,
        itemY: list = ['A', 'B', 'C', 'D', 'E'],
        valueX: list = [1, 2, 3, 2, 1],
        graph_title: str = "new graph",
        save_path: str = str(
            # from fchooser import *
            # fchooser.py
            fileSaver(
                # title: str
                'Save Graph',
                # filetypes: list
                [('PNG File', '*.png')],
                # defaultextension: str
                ".png",
                # initialfile: str
                str(time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime()))
            )
        )):
    fig = plt.figure(figsize=figSize_wid_len, dpi=dpi)
    df = pd.DataFrame({'Group': itemY, 'Value': valueX})
    plt.barh(y=df.Group, width=df.Value)
    plt.title(graph_title)
    fig.savefig(save_path, dpi=dpi)

quartile1_itemY_valueX(figSize_wid_len=(10, 15), dpi=100)
