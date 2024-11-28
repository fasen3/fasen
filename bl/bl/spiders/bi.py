# 主要用于解析网站内容，并将解析后的数据传给items pipeline
import scrapy
import json
from bl.bl.items import BlItem


class BiSpider(scrapy.Spider):
    name = 'bi'
    allowed_domains = ['bilibili.com']
    # start_urls默认为'http：//'+allowed_domains[0]
    # 要重写start_urls，把排行榜页面的url列表赋值给start_urls
    start_urls = [
        'https://www.bilibili.com/v/popular/rank/all',  # 全站
        'https://www.bilibili.com/v/popular/rank/guochuang',  # 国创相关
        'https://www.bilibili.com/v/popular/rank/douga',  # 动画
        'https://www.bilibili.com/v/popular/rank/music',  # 音乐
        'https://www.bilibili.com/v/popular/rank/dance',  # 舞蹈
        'https://www.bilibili.com/v/popular/rank/game',  # 游戏
        'https://www.bilibili.com/v/popular/rank/knowledge',  # 知识
        'https://www.bilibili.com/v/popular/rank/tech',  # 科技
        'https://www.bilibili.com/v/popular/rank/sports',  # 运动
        'https://www.bilibili.com/v/popular/rank/car',  # 汽车
        'https://www.bilibili.com/v/popular/rank/life',  # 生活
        'https://www.bilibili.com/v/popular/rank/food',  # 美食
        'https://www.bilibili.com/v/popular/rank/animal',  # 动物圈
        'https://www.bilibili.com/v/popular/rank/kichiku',  # 鬼畜
        'https://www.bilibili.com/v/popular/rank/fashion',  # 时尚
        'https://www.bilibili.com/v/popular/rank/ent',  # 娱乐
        'https://www.bilibili.com/v/popular/rank/cinephile',  # 影视
        'https://www.bilibili.com/v/popular/rank/origin',  # 原创
        'https://www.bilibili.com/v/popular/rank/rookie',  # 新人
        # # "全站"
        # 'https://api.bilibili.com/x/web-interface/ranking/v2?rid=0&type=all',
        # # "国创相关":
        # 'https://api.bilibili.com/x/web-interface/ranking/v2?rid=168&type=all',
        # # "动画":
        # 'https://api.bilibili.com/x/web-interface/ranking/v2?rid=1&type=all',
        # # "音乐":
        # 'https://api.bilibili.com/x/web-interface/ranking/v2?rid=3&type=all',
        # # "舞蹈":
        # 'https://api.bilibili.com/x/web-interface/ranking/v2?rid=129&type=all',
        # # "游戏":
        # 'https://api.bilibili.com/x/web-interface/ranking/v2?rid=4&type=all',
        # # "知识":
        # 'https://api.bilibili.com/x/web-interface/ranking/v2?rid=36&type=all',
        # # "科技":
        # 'https://api.bilibili.com/x/web-interface/ranking/v2?rid=188&type=all',
        # # "运动":
        # 'https://api.bilibili.com/x/web-interface/ranking/v2?rid=234&type=all',
        # # "汽车":
        # 'https://api.bilibili.com/x/web-interface/ranking/v2?rid=223&type=all',
        # # "生活":
        # 'https://api.bilibili.com/x/web-interface/ranking/v2?rid=160&type=all',
        # # "美食":
        # 'https://api.bilibili.com/x/web-interface/ranking/v2?rid=211&type=all',
        # # "动物圈":
        # 'https://api.bilibili.com/x/web-interface/ranking/v2?rid=217&type=all',
        # # "鬼畜":
        # 'https://api.bilibili.com/x/web-interface/ranking/v2?rid=119&type=all',
        # # "时尚":
        # 'https://api.bilibili.com/x/web-interface/ranking/v2?rid=155&type=all',
        # # "娱乐":
        # 'https://api.bilibili.com/x/web-interface/ranking/v2?rid=5&type=all',
        # # "原创":
        # 'https://api.bilibili.com/x/web-interface/ranking/v2?rid=0&type=origin',
        # # "新人":
        # 'https://api.bilibili.com/x/web-interface/ranking/v2?rid=0&type=rookie'
    ]

    def parse(self, response):
        # 获取当前爬取的榜单名称
        rank_tab = response.xpath('//ul[@class="rank-tab"]/li[@class="rank-tab--active"]/text()').getall()[0]
        print('⭐' * 3, '当前爬取榜单为:', rank_tab, '=' * 50)

        # 视频的信息都放在li标签中，这里先获取所有的li标签
        # 之后遍历rank_lists获取每个视频的信息
        rank_lists = response.xpath('//ul[@class="rank-list"]/li')
        for rank_list in rank_lists:
            # 排名
            rank_num = rank_list.xpath('@data-rank').get()
            # 视频名称
            title = rank_list.xpath('div/div[@class="info"]/a/text()').get()
            # 视频的id
            id = rank_list.xpath('@data-id').get()
            # 视频链接
            href = rank_list.xpath('div/div[@class="info"]/a/@href').get()
            # 拼接详情页api的url
            # 各种数据量
            Detail_link = f'https://api.bilibili.com/x/web-interface/archive/stat?aid={id}'
            # tag
            Labels_link = f'https://api.bilibili.com/x/tag/archive/tags?aid={id}'
            # up主
            author = rank_list.xpath('div/div[@class="info"]/div[@class="detail"]/a/span/text()').get()
            # up主页链接
            au_href = rank_list.xpath('div/div[@class="info"]/div[@class="detail"]/a/@href').get()
            # 如用requests库发送请求，要再写多一次请求头
            # 因此我们继续使用Scrapy向api发送请求
            # 这里创建一个字典去储存我们已经抓到的数据
            # 这样能保证我们的详细数据和排行数据能一一对应无需进一步合并
            # 如果这里直接给到Scrapy的Item的话，最后排行页的数据会有缺失
            items = {
                'rank_tab': rank_tab,
                'rank_num': rank_num,
                'title': title,
                'id': id,
                'author': author,
                'au_href': au_href,
                'href': href,
                'Detail_link': Detail_link,
            }
            # 将api发送给调度器进行详情页的请求，通过meta传递排行页数据
            yield scrapy.Request(url=Labels_link, callback=self.Get_labels, meta={'item': items}, dont_filter=True)

    def Get_labels(self, response):
        # 获取热门标签数据
        items = response.meta['item']
        # 各种数据量详情页
        Detail_link = items['Detail_link']
        # 解析json数据
        html = json.loads(response.body)
        tags = html['data']  # 视频标签数据
        # 利用逗号分割列表，返回字符串
        tag_name = ','.join([i['tag_name'] for i in tags])
        items['tag_name'] = tag_name
        yield scrapy.Request(url=Detail_link, callback=self.Get_detail, meta={'item': items}, dont_filter=True)

    def Get_detail(self, response):
        # 获取排行页数据
        items = response.meta['item']
        rank_tab = items['rank_tab']
        rank_num = items['rank_num']
        title = items['title']
        id = items['id']
        au_href = items['au_href']
        author = items['author']
        href = items['href']
        tag_name = items['tag_name']

        # 解析json数据
        html = json.loads(response.body)

        # 获取详细播放信息
        stat = html['data']

        view = stat['view']  # 播放量
        danmaku = stat['danmaku']  # 弹幕量
        reply = stat['reply']  # 评论数
        favorite = stat['favorite']  # 收藏数
        coin = stat['coin']  # 投币数
        share = stat['share']  # 分享数
        like = stat['like']  # 点赞数

        # 把所有爬取的信息传递给Item
        item = BlItem(
            rank_tab=rank_tab,
            rank_num=rank_num,
            title=title,
            href=href,
            id=id,
            author=author,
            au_href=au_href,
            view=view,
            danmaku=danmaku,
            reply=reply,
            favorite=favorite,
            coin=coin,
            share=share,
            like=like,
            tag_name=tag_name
        )
        yield item
