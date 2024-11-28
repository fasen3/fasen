#⭐Scrapy框架 

✅scrapy.cfg ：项目的配置文件

✅bl/bl ：项目的Python模块，将会从这里引用代码

✅items.py ：项目的目标文件

✅pipelines.py ：项目的管道文件

✅settings.py ：项目的设置文件

✅spiders/ ：存储获取代码目录

✅bi.py ：通过命令新建的文件

##♻数据流：

1️⃣ScrapyEngine打开一个网站，找到处理该网站的Spider，并向该Spider请求第一个(批)要爬取的url(s)；

2️⃣ScrapyEngine向调度器请求第一个要爬取的url，并加入到Schedule作为请求以备调度；

3️⃣ScrapyEngine向调度器请求下一个要爬取的url；

4️⃣Schedule返回下一个要爬取的url给ScrapyEngine，ScrapyEngine通过DownloaderMiddlewares将url转发给Downloader；

5️⃣页面下载完毕，Downloader生成一个页面的Response，通过DownloaderMiddlewares发送给ScrapyEngine；

6️⃣ScrapyEngine从Downloader中接收到Response，通过SpiderMiddlewares发送给Spider处理；

7️⃣Spider处理Response并返回提取到的Item以及新的Request给ScrapyEngine；

8️⃣ScrapyEngine将Spider返回的Item交给ItemPipeline，将Spider返回的Request交给Schedule进行从第二步开始的重复操作，直到调度器中没有待处理的Request，ScrapyEngine关闭。


###⭐爬虫目标

1、对ajax异步加载的网页进行抓包，通过抓取Request URL访问异步加载数据

2、使用Scrapy框架进行数据采集

3、利用scrapy.Request向api发送请求并通过meta传递已获取的排行页数据

4、利用Scrapy内置的CsvItemExporter将数据存储到csv中

###⭐数据分析

1、数据预清洗。了解csv中的数据结构，有逻辑地进行分类聚合

bilibili.csv

| #   | Column   | None-Null Count | Dtype   |
|-----|----------|-----------------|---------|
| 0   | au_href  | 1901 non-nul    | object  |
| 1   | author   | 1900 non-null   | object  |
| 2   | coin     | 1900 non-null   | float64 |
| 3   | danmaku  | 1900 non-null   | float64 |
| 4   | favorite | 1900 non-null   | object  |
| 5   | href     | 1900 non-null   | object  |
| 6   | id       | 1900 non-null   | float64 |
| 7   | like     | 1900 non-null   | float64 |
| 8   | rank_num | 1900 non-null   | object  |
| 9   | rank_tab | 1900 non-null   | object  |
| 10  | reply    | 1900 non-null   | float64 |
| 11  | share    | 1900 non-null   | object  |
| 12  | tag_name | 1900 non-null   | object  |
| 13  | title    | 1900 non-null   | object  |
| 14  | view     | 1900 non-null   | float64 |

RangeIndex: 1901 entries, 0 to 1900
Data columns (total 15 columns)
dtypes: float64(6), object(9)
memory usage: 222.9+ KB
采集到的数据一共15列，1900行，没有缺失值

全站.csv

| #   | Column   | None-Null Count | Dtype   |
|-----|----------|-----------------|---------|
| 0   | au_href  | 100 non-null    | object  |
| 1   | author   | 100 non-null    | object  |
| 2   | coin     | 100 non-null    | float64 |
| 3   | danmaku  | 100 non-null    | float64 |
| 4   | favorite | 100 non-null    | int64   |
| 5   | href     | 100 non-null    | object  |
| 6   | id       | 100 non-null    | float64 |
| 7   | like     | 100 non-null    | float64 |
| 8   | rank_num | 100 non-null    | int64   |
| 9   | rank_tab | 100 non-null    | object  |
| 10  | reply    | 100 non-null    | float64 |
| 11  | share    | 100 non-null    | int64   |
| 12  | title    | 100 non-null    | object  |
| 13  | view     | 100 non-null    | float64 |


RangeIndex: 100 entries, 0 to 99
Data columns (total 14 columns)
dtypes: float64(6), int64(3), object(6)
memory usage: 11.8+ KB

####🟢dataClean.py 得出top100情况.csv与各分类情况.csv

2、使用top.csv可视化数据

--各分区占比情况可视化：玫瑰图（展示播放量top100的各分区个数）

--各分区弹幕分享评论平均情况可视化：柱状图折线图组合图（展示播放量top100的各分区三种情况）

--各分区平均播放量情况可视化：柱状图（展示播放量top100的各分区播放量）

--各分区平均三连情况可视化：雷达图（展示播放量top100的各分区三连量）

3、使用各区分类情况.csv可视化数据

--播放量均值情况可视化：折线图（展示各分区的播放量）

--三连量均值情况可视化：三个折线图的组合（展示各分区三连量）

4、使用bilibili.csv做词云图与关联度大的Top100各分区占比情况

4.1、词云图制作

4.2、灰色关联度计算指标.py