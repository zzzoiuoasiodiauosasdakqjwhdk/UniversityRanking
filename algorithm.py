# -*- coding = utf-8 -*-
# encoding: utf-8
# @Time : 2021.12.10 19:09
# @Author : https://github.com/SynFUN / https://github.com/SynthesisDu
# @File : algorithm.py
# @Software : PyCharm

def expected_value(X, P):
    if len(X) != len(P):
        return False, 0
    E = 0
    for i in range(len(X)):
        E += X[i] * P[i]
    return True, E
