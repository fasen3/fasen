#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023-4-23 22:19
# @Author  : SHANNON
# @File    : dataClean-All.py
# @Description :分区存储Top100的数据
# 数据预清洗
import pandas as pd

df = pd.read_csv('../bilibili.csv',error_bad_lines=False)
l=['全站','国创相关','动画','音乐','舞蹈','游戏','知识','科技','运动','汽车','生活','美食','动物圈','鬼畜','时尚','娱乐','影视','原创','新人']

for index in range(0,19):
    df_all=df[df['rank_tab'].isin([l[index]])]
    df_all.to_csv('csv/'+l[index]+'.csv',encoding='utf-8',index=False)

# df=pd.read_csv("csv/娱乐.csv")
# print(df.info())