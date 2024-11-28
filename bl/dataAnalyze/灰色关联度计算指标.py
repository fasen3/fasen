#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023-4-23 21:39
# @Author  : SHANNON
# @File    : 灰色关联度计算指标.py
# @Description :

# python3不支持file()打开文件,只能用open()

# 假设B站高排名可能是与播放、评论、收藏、投币、分享、点赞几个因素相关的，
# 那么我们想知道高排名与这几个因素中的哪个相对来说更有关系，而哪个因素相对关系弱一点，
# 把这些因素排个序，得到一个分析结果，我们就可以知道哔哩哔哩高排名，与因素中的哪些更相关，
# 因而也就可以看出观众的一键三连的作用以及up主们更应该求的是赞、币亦或是其他。


# 灰色关联度分析版本
import pandas as pd
import numpy as np
from pyecharts import options as opts
from pyecharts.charts import Graph
import matplotlib as mpl
from pyecharts.render import snapshot, make_snapshot
from pyecharts.render.engine import render

mpl.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题

# 读取数据
df = pd.read_csv('csv/全站.csv')
# print(df.info())
rank_num = df['rank_num'].tolist()[::-1]
coin = df['coin'].tolist()
favorite = df['favorite'].tolist()
like = df['like'].tolist()
reply = df['reply'].tolist()
share = df['share'].tolist()
view = df['view'].tolist()

# 定义子母序列
mom_ = rank_num
son_ = [coin, favorite, like, reply, share, view]

mom_ = np.array(mom_)
son_ = np.array(son_)

# 对指标数据进行无量纲化
son_ = son_.T / son_.mean(axis=1)
mom_ = (mom_ / mom_.mean())
# print(mom_)
# print(son_)

# 遍历子序列中的所有数据计算被评价序列与参考序列的绝对差
for i in range(son_.shape[1]):
    son_[:, i] = abs(son_[:, i] - mom_.T)

# 取出绝对差中的最大最小值
Mmin = son_.min()
Mmax = son_.max()
# print(Mmin, Mmax)

# 计算关联度系数,0.05为分辨系数，越小区分能力越大,最好取0.05
cors = (Mmin + 0.05 * Mmax) / (son_ + 0.05 * Mmax)
# print(cors)
# 求均值得到灰色关联度，扩大数值方便研究
Mmean = cors.mean(axis=0) * 180

nodes = [
    {"name": "投币", "symbolSize": Mmean[0]},
    {"name": "收藏", "symbolSize": Mmean[1]},
    {"name": "点赞", "symbolSize": Mmean[2]},
    {"name": "评论", "symbolSize": Mmean[3]},
    {"name": "分享", "symbolSize": Mmean[4]},
    {"name": "播放", "symbolSize": Mmean[5]},
]
print("=========", nodes)

# 绘制graph图
links = []
for i in nodes:
    for j in nodes:
        links.append({"source": i.get("name"), "target": j.get("name")})
# print(links)

c = (
    Graph()
        .add(
        "",
        nodes,
        links,
        repulsion=30000,  # 线长
    )
)
c.set_colors('#006600')
# ['#BF0060','#02F78E','#FF95CA','#96FED1','FFD9EC','D7FFEE']
# plt.plot(links,'*-',c='red')
# c.render_notebook()
c.render('../../static/s/html/计算指标.html')
# # 运行画图并保存为png
# make_snapshot(snapshot, render(c), '../../static/雷达图.png')
