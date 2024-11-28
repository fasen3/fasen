#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023-4-25 15:53
# @Author  : SHANNON
# @File    : 各分区三连均值.py
# @Description :
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
    like=df['like'].tolist()
    coin=df['coin'].tolist()
    favorite=df['favorite'].tolist()
    return genre,like,coin,favorite

# 绘制折线图
def line_base(v1,v2,v3,v4):
    line1=(
        Line(init_opts=opts.InitOpts(width='1000px', height='700px'))
        .add_xaxis(v1)
        .add_yaxis(
            series_name="点赞",
            y_axis=v2
        )
            .set_global_opts(
            # 将分区名旋转45度来保证所有分区都能显示
            xaxis_opts=opts.AxisOpts(axislabel_opts={'rotate': 45})
        )
        .extend_axis(  # 设置次坐标轴
            yaxis=opts.AxisOpts(
                name="",  # 次坐标轴名称
                type_="value",  # 次坐标手类型
                is_show=True,  # 是否显示网格
                axisline_opts=opts.AxisLineOpts(is_show=False,  # y轴线不显示
                                                linestyle_opts=opts.LineStyleOpts(color='#f6c065')),  # 设置线颜色, 字体颜色也变
                axistick_opts=opts.AxisTickOpts(is_show=False),  # 刻度线不显示
                axislabel_opts=opts.LabelOpts(formatter="{value}"),  # 次坐标轴数据显示格式
            )
        )
            .set_global_opts(title_opts=opts.TitleOpts(#title="各分区top100三连可视化",  # 标题
                                                       title_textstyle_opts=opts.TextStyleOpts(font_size=20),  # 主标题字体大小
                                                       # subtitle="看图",  # 次坐标轴
                                                       pos_left='6%'),  # 标题位置
                             legend_opts=opts.LegendOpts(is_show=False),  # 不显示图例
                             tooltip_opts=opts.TooltipOpts(trigger="axis"),  # 提示框
                             yaxis_opts=opts.AxisOpts(type_="value",  # y轴类型-连续数据
                                                      name='单位: 数量',  # y轴名称
                                                      name_location='middle',  # y轴名称位置
                                                      name_gap=50,  # y轴名称距离轴线距离
                                                      axistick_opts=opts.AxisTickOpts(is_show=False),  # 刻度线
                                                      axisline_opts=opts.AxisLineOpts(is_show=False),  # y轴线
                                                      splitline_opts=opts.SplitLineOpts(is_show=True),  # y轴网格线
                                                      axislabel_opts=opts.LabelOpts(formatter="{value}")),
                             # y轴标签显示方式-刻度标签的内容格式器，支持字符串模板和回调函数两种形式
                             )
    )
    line2=(
        Line()
        .add_xaxis(v1)
        .add_yaxis(
            series_name="投币",
            y_axis=v3,
            is_smooth=True,
            yaxis_index=1
        )
            .set_global_opts(
            # 将分区名旋转45度来保证所有分区都能显示
            xaxis_opts=opts.AxisOpts(axislabel_opts={'rotate': 45})
        )
    )
    line3=(
        Line()
        .add_xaxis(v1)
        .add_yaxis(
            series_name="收藏",
            y_axis=v4,
            yaxis_index=1
        )
            .set_global_opts(
            # 将分区名旋转45度来保证所有分区都能显示
            xaxis_opts=opts.AxisOpts(axislabel_opts={'rotate': 45})
        )
    )
    a=line1.overlap(line2)
    b=a.overlap(line3)
    return b

if __name__ == '__main__':
    genre,like,coin,favorite=open_file()
    line_base(genre,like,coin,favorite).render('../../../static/s/html/各分区三连均值情况可视化.html')

