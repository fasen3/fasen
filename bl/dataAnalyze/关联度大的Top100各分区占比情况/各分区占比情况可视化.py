
import pandas as pd
from pyecharts import options as opts
from pyecharts.charts import Pie

# 数据预清洗
def get_date():
    df = pd.read_csv('../../bilibili.csv', error_bad_lines=False)
    print(df.info())
    # 波浪线~表示不选取该部分
    df_without_all = df[~df['rank_tab'].isin(['全站'])]
    return df_without_all


# 统计点赞量top100各区占比情况
def count_genre_top100(df):
    # 排序，切片，获取rank_tab列
    # 对预处理好的df_without_all按照点赞量降序排序；对DataFrame进行切片处理，获取前100项；获取分区名列（columns=‘rank_tab’）；
    genres_like_Series = df.sort_values(by='like', ascending=False)[:100]['rank_tab']
    # 使用value_counts()方法快速求出各分区出现的次数
    # 通过.value_counts()方法，得到一个index为分区名，values为频次的Series类型
    geners_like_count = genres_like_Series.value_counts()
    print(geners_like_count)
    print(type(geners_like_count))
    return geners_like_count


color_series = ['#FFFFCC','#CCFFFF','#FFCCCC','#FFFF99','#CCCCFF',
'#FF9966','#FF6666','#CCFF99','#99CC99','#66CCCC',
'#2C6BA0','#2B55A1','#2D3D8E','#44388E','#6A368B'
'#7D3990','#A63F98','#C31C88','#D52178','#D5225B',
'#D02C2A','#D44C2D','#F57A34','#FA8F2F','#D99D21',
'#CF7B25','#CF7B25','#CF7B25']

# 绘制玫瑰图
def pie_rosrtype(df):
    c = (
        Pie(init_opts=opts.InitOpts(width='1000px', height='700px'))
            .add(
            '',
            # 添加数据，数据类型结构：[['生活', 30], ['动画', 20]]
            [list(z) for z in zip(df.index, df)],
            radius=['30%', '75%'],  # radius模式：用扇形圆心角展现数据的百分比，通过半径展现数据大小。
            center=['50%', '50%'],  # area模式：所有扇形圆心角相同，仅通过半径展现数据大小。
            rosetype="radius",
        )
            .set_colors(color_series)
            # 设置标签，展现形式为 标签：数值:百分比
            .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}:{c}:{d}%"))
    )
    return c


if __name__ == '__main__':
    df_without_all = get_date()
    count_genre = count_genre_top100(df_without_all)
    pie = pie_rosrtype(count_genre)
    pie.render('../../../static/s/html/排名关联度最大的各区占比情况.html')
