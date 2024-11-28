# 读取scv数据，获取分类名和平均播放量
# 构建分类名和平均播放量的列表
# 创建普通的柱状图
# 在普通柱状图中加入Javascript语句制作渐变色
# 利用snapshot_selenium 将html转存为png

import pandas as pd
# 构建图表用的库
from pyecharts import options as opts
from pyecharts.charts import Bar

# 调用js语句所需库
from pyecharts.commons.utils import JsCode

# 转存为png所需库
from pyecharts.render import make_snapshot
from snapshot_selenium import snapshot


# 读取数据
def open_file():
    df = pd.read_csv('../top100情况.csv')
    title = df['genre'].tolist()
    view=df['view'].tolist()
    return title, view


# 制作图表
def bar_border_radius(v1, v2):
    bar = (
        Bar(init_opts=opts.InitOpts(width='1000px', height='700px'))
        .add_xaxis(v1)
            .add_yaxis(
            series_name="播放量",  # 柱形图y轴坐标
            y_axis=v2,
            label_opts=opts.LabelOpts(is_show=True, position='top', formatter="{c}"),  # 显示数据标签
            itemstyle_opts=opts.ItemStyleOpts(color="#78c4d4", opacity=0.4),  # 柱形图颜色及透明度
        )
        .set_global_opts(
            xaxis_opts=opts.AxisOpts(axislabel_opts={'rotate': 45}
        )
    )
)
    return bar


if __name__ == '__main__':
    title, view = open_file()
    # 正常情况下在调用制作图表的函数后添加.render()即可生成html文件
    bar_border_radius(title,view).render('../../../static/s/html/Top100平均播放量情况.html')
    # # 这里一步将生成图表和转存为png
    # make_snapshot(snapshot, bar_border_radius(title, view).render(), '全站top100播放量.png')
