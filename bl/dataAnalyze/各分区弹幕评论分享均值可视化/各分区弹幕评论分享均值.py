#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023-4-25 16:19
# @Author  : SHANNON
# @File    : 各分区弹幕评论分享均值.py
# @Description :
import pandas as pd
from pyecharts import options as opts
from pyecharts.charts import Line  # 导入折线图
from pyecharts.charts import Bar  # 导入柱状图
from pyecharts.commons.utils import JsCode
# 下面两个模块用于将html转为png
from pyecharts.render import make_snapshot
from snapshot_selenium import snapshot


def open_file():
    df = pd.read_csv('../各分类情况.csv')
    genre = df['genre'].tolist()
    danmaku = df['danmaku'].tolist()
    share = df['share'].tolist()
    reply = df['reply'].tolist()
    return genre, danmaku, share, reply


# 画图
def comp_base(v1, v2, v3, v4):
    bar = (
        Bar(init_opts=opts.InitOpts(width='1000px', height='700px'))
            .add_xaxis(v1)
            .add_yaxis(
            series_name="弹幕数",  # 柱形图y轴坐标
            y_axis=v2,
            label_opts=opts.LabelOpts(is_show=True, position='top', formatter="{c}"),  # 显示数据标签
            itemstyle_opts=opts.ItemStyleOpts(color="#78c4d4", opacity=0.4),  # 柱形图颜色及透明度
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
            .set_global_opts(title_opts=opts.TitleOpts(#title="各分区平均弹幕分享评论可视化",  # 标题
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

    line2 = (
        Line()
            .add_xaxis(v1)  # x轴
            .add_yaxis(
            series_name="评论数",  # 显示名称
            yaxis_index=1,  # 次坐标
            is_smooth=True,  # 线条样式 ,是否设置成圆滑曲线，默认为非圆滑
            y_axis=v4,
            itemstyle_opts=opts.ItemStyleOpts(color="#f6c065"),  # 标记的颜色
            linestyle_opts=opts.LineStyleOpts(width=3, color='#f6c065'),  # 线条颜色和宽度
        )
            .set_global_opts(
            # 将分区名旋转45度来保证所有分区都能显示
            xaxis_opts=opts.AxisOpts(axislabel_opts={'rotate': 45})
        )
    )
    line3 = (
        Line()
            .add_xaxis(v1)
            .add_yaxis(
            series_name="分享数",
            yaxis_index=1,
            y_axis=v3,
            itemstyle_opts=opts.ItemStyleOpts(color="#5793f3"),
            linestyle_opts=opts.LineStyleOpts(width=3, color="#5793f3")
        )
            .set_global_opts(
            # 将分区名旋转45度来保证所有分区都能显示
            xaxis_opts=opts.AxisOpts(axislabel_opts={'rotate': 45})
        )
    )
    a = bar.overlap(line2)
    b = a.overlap(line3)
    return b


if __name__ == '__main__':
    genre, danmaku, share, reply = open_file()
    # 正常情况下在调用制作图表的函数后添加.render()即可生成html文件
    comp_base(genre, danmaku, share, reply).render('../../../static/s/html/各分区弹幕评论分享平均情况.html')
    # # 运行画图并保存为png
    # make_snapshot(snapshot, reder_base(coins, like, favorite).render(), '雷达图.png')
