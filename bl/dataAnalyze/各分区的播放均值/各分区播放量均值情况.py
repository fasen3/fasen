#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023-4-23 22:25
# @Author  : SHANNON
# @File    : 播放量均值.py
# @Description :

import pandas as pd
import pyecharts.options as opts
from pyecharts.charts import Line
from pyecharts.render import make_snapshot
from snapshot_selenium import snapshot

def open_file():
    df=pd.read_csv('../各分类情况.csv')
    genre=df['genre'].tolist()
    view=df['view'].tolist()
    #对数据进行一定的缩放
    view=[i//10000 for i in view]
    return genre,view

# 绘制折线图
def line_base(genre,view):
    c=(
        Line(init_opts=opts.InitOpts(width='1000px', height='700px'))
        .add_xaxis(genre)
        .add_yaxis(
            '播放量 单位：千万',
            view,
            #设置标签指出最高值
            markpoint_opts=opts.MarkPointOpts(data=[opts.MarkPointItem(type_="max")]),
        )
        .set_global_opts(

            #将分区名旋转45度来保证所有分区都能显示
            xaxis_opts=opts.AxisOpts(axislabel_opts={'rotate':45})
        )
    )
    return c

if __name__ == '__main__':
    genre,view=open_file()
    line_base(genre,view).render('../../../static/s/html/各分区播放量均值.html')

