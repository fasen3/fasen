#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023-4-22 23:05
# @Author  : SHANNON
# @File    : dataClean.py
# @Description :数据清洗
import csv
import pandas as pd


# fields=['//space.bilibili.com/109939424',
#         ' 范冰冰BAR',
#         '433','256','3444','//www.bilibili.com/video/BV17h4y1p7jR','612811058','32904','13','娱乐','711','1546',"美女,香港,范冰冰,演员,杂志",'【范冰冰】香港的邮轮上，完成杂志收尾拍摄','292106'
# ]
# with open('../bilibili.csv','a',encoding='utf-8') as fd:
#     writer=csv.writer(fd)
#     writer.writerow(fields)

# 数据预清洗
def get_date():
    df = pd.read_csv('../bilibili.csv', error_bad_lines=False)
    # 波浪线~表示不选取该部分
    df_without_all = df[~df['rank_tab'].isin(["全站"])]
    # print(df_without_all['favorite'].tolist())
    return df_without_all


# 获取各区平均情况数据处理
def genre_mean(df):
    # by：表示根据什么字段或者索引进行排序，可以是一个或多个
    # axis：排序是在横轴还是纵轴，默认是纵轴axis=0
    # ascending：排序结果是升序还是降序，默认是升序
    # inplace：表示排序的结果是直接在原数据上的就地修改还是生成新的DatFrame
    # kind：表示使用排序的算法，快排quicksort,，归并mergesort， 堆排序heapsort，稳定排序stable ，默认是 ：快排quicksort
    # na_position：缺失值的位置处理，默认是最后，另一个选择是首位
    # ignore_index：新生成的数据帧的索引是否重排，默认False（采用原数据的索引）
    # key：排序之前使用的函数
    # 将点赞量按照降序进行排列
    genres_rank_df = df.sort_values(by='like', ascending=False)[:100]
    # print(genres_rank_df)
    # 以分区分组计算平均播放量，将数据从float转为int来去除小数点
    genre_mean = genres_rank_df.groupby('rank_tab').mean().astype('int')
    # print(genre_mean)
    # 将genre作为csv文件中的表头
    genre_mean['genre'] = genre_mean.index
    genre_mean.to_csv('top100情况.csv', encoding='utf-8-sig', index=False)


# 各分类情况数据处理
def get_rank_mean(df):
    # 按照分区名称分组
    df_group = df.groupby(by='rank_tab')
    # 生成的文件中剔除id与rank_num两个数字，因为这类数字是要进行数据处理而不涉及到这两列
    rang_tab_mean = df_group.mean().drop(['id', 'rank_num'], axis=1).astype('int')
    rang_tab_mean['genre'] = rang_tab_mean.index
    rang_tab_mean.to_csv('各分类情况.csv', encoding='utf-8-sig', index=False)


if __name__ == '__main__':
    df_without_all = get_date()
    genre_mean(df_without_all)
    get_rank_mean(df_without_all)
