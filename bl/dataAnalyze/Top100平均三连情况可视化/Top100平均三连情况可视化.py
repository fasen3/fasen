#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023-4-24 22:25
# @Author  : SHANNON
# @File    : Top100平均三连情况可视化.py
# @Description :

# 读取csv数据，获取投币、点赞、收藏的平均数值，并各自创建一个列表用于储存数据
# 构建图表
# 利用selenium将html转化为png
import pandas as pd
from pyecharts import options as opts
from pyecharts.charts import Radar
# 下面两个模块用于将html转为png
from pyecharts.render import make_snapshot
from snapshot_selenium import snapshot


# 读取数据并构建雷达图的数据结构
def bulid_data():
    df = pd.read_csv('../top100情况.csv')
    # 这里的print是帮助提取genre来批量构建雷达图的标签
    print(df['genre'].tolist())
    # out：['动画', '娱乐', '影视', '时尚', '游戏', '生活', '科技', '音乐', '鬼畜']
    # 雷达图接收的数据是列表类型，这里使用.tolist方法将Series转化为列表
    coins = [df['coin'].tolist()]
    like = [df['like'].tolist()]
    favorite = [df['favorite'].tolist()]
    return (coins, like, favorite)


# 画图
def reder_base(v1, v2, v3):
    c = (
        Radar(init_opts=opts.InitOpts(width='1000px', height='700px'))
            .add_schema(
            schema=[
                opts.RadarIndicatorItem(name='动物圈', max_=650000),
                opts.RadarIndicatorItem(name='原创', max_=650000),
                opts.RadarIndicatorItem(name='国创相关', max_=650000),
                opts.RadarIndicatorItem(name='娱乐', max_=650000),
                opts.RadarIndicatorItem(name='影视', max_=650000),
                opts.RadarIndicatorItem(name='新人', max_=650000),
                opts.RadarIndicatorItem(name='游戏', max_=650000),
                opts.RadarIndicatorItem(name='生活', max_=650000),
                opts.RadarIndicatorItem(name='知识', max_=650000),
                opts.RadarIndicatorItem(name='科技', max_=650000),
                opts.RadarIndicatorItem(name='美食', max_=650000),
                opts.RadarIndicatorItem(name='舞蹈', max_=650000),
                opts.RadarIndicatorItem(name='运动', max_=650000),
                opts.RadarIndicatorItem(name='音乐', max_=650000),
                opts.RadarIndicatorItem(name='鬼畜', max_=650000),
            ]
        )
            # 添加指标，设置线条颜色
            .add('投币', v1, color='#FF6699')
            .add('点赞', v2, color='#00AEEC')
            .add('收藏', v3, color='#FFB027')
            .set_series_opts(
            # 不显示指标数值
            label_opts=opts.LabelOpts(is_show=False),
            # 设置线条格式，宽度为3，样式为虚线
            linestyle_opts=opts.LineStyleOpts(width=3, type_='dotted'),
        )
    )
    return c


if __name__ == '__main__':
    coins, like, favorite = bulid_data()
    # 正常情况下在调用制作图表的函数后添加.render()即可生成html文件
    reder_base(coins,like,favorite).render('../../../static/s/html/Top100平均三连的雷达图.html')
    # # 运行画图并保存为png
    # make_snapshot(snapshot, reder_base(coins, like, favorite).render(), '雷达图.png')
