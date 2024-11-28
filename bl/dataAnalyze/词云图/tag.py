#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023-4-22 23:06
# @Author  : SHANNON
# @File    : tag.py
# @Description :将标签列先转化为一个一维的列表或数组，求出唯一的标签，最后统计每一个唯一标签出现的次数
import pandas as pd
from pyecharts import options as opts
from pyecharts.charts import WordCloud


# 从df_without_all的tag_name列提取热门标签
# 将热门标签数据解嵌套为一维的列表
# 将列表转化为Series，并调用.value_counts()方法，赋值给tags_value
# 将tags_value作为参数制作词云

# 获取标签
def get_date():
    df = pd.read_csv('../../bilibili.csv', error_bad_lines=False)
    # print(df.info())
    # 波浪线~表示不选取该部分
    df_without_all = df[~df['rank_tab'].isin(['全站'])]
    return df_without_all


def build_tags_value(df):
    # 获取tag_name标签下的数据
    # 利用join为列表解嵌套，获得字符串
    # 通过逗号对字符串进行拆分，获得无嵌套列表
    tag_list = ','.join(df['tag_name']).split(',')
    # 构造Series并调用.value_counts()
    tags_count = pd.Series(tag_list).value_counts()
    return tags_count


def wordcliud_base(df):
    c = (
        WordCloud()
            .add(
            '',
            [list(z) for z in zip(df.index, df)],
            word_size_range=[5, 100],
            shape='circle',
            # mask_image='bilibili.png'
        )
    )
    return c


if __name__ == '__main__':
    df_without_all = get_date()
    df_1 = df_without_all.groupby(by='rank_tab')['title'].count()
    # print(df_1)
    tags_count = build_tags_value(df_without_all)
    wordcliud_base(tags_count).render('../../../static/s/html/热门标签词云图.html')
    # make_snapshot(snapshot,wordcliud_base(tags_count).render(),'热门标签词云.png')
