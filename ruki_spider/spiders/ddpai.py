import scrapy
import json
import os

class DdpaiSpider(scrapy.Spider):
    name = "ddpai"

    def start_requests(self):
        # 默认值是0，从上一次爬取数据里读取计数器
        count = 0
        with open("ddpai/tmp/ddpai.json", "r") as new_file:
            new_items = json.load(new_file)
            sorted(new_items, key=lambda item: item["id"])
            if len(new_items) > 0:
                count = int(new_items[-1]["id"])
        # 开始爬取数据
        for i in range(count + 1, count + 1000):
            url = 'http://app.ddpai.com/d/api/v1/storage/res/fragment/{}'.format(i);
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        jsonresponse = json.loads(response.text)
        # 媒体信息判空
        if "resobjs" not in jsonresponse:
            # print("no resobjs")
            return
        ress = jsonresponse["resobjs"]
        if not ress:
            # print("empty resobjs")
            return
        res = ress[0]
        if "type" not in res or res["type"] != 2:
            # print("resobj type not match")
            return
        # 其他信息判空
        if "id" not in jsonresponse:
            # print("no item id")
            return
        # 媒体路径
        if "remotePath" not in res or not res["remotePath"]:
            return
        item_id = jsonresponse["id"]
        path = res["remotePath"]
        # 描述
        des = ""
        if "des" in jsonresponse:
            des = jsonresponse["des"]
        # 经纬度
        coords = []
        if "longitude" in jsonresponse and "latitude" in jsonresponse:
            coords = [jsonresponse["longitude"], jsonresponse["latitude"]]
        # 位置
        location = ""
        if "location" in jsonresponse:
            location = jsonresponse["location"]
        # 评论数
        comments = 0
        if "commentCount" in jsonresponse:
            comments = jsonresponse["commentCount"]
        # 浏览数
        views = 0
        if "showViewedCount" in jsonresponse:
            views = jsonresponse["showViewedCount"]
        # 赞数
        likes = 0
        if "favCount" in jsonresponse:
            likes = jsonresponse["favCount"]
        # 类型
        item_type = ""
        if "typeId" in jsonresponse:
            item_type = jsonresponse["typeId"]

        yield {
            "id": item_id,
            "des": des,
            "coords": coords,
            "location": location,
            "path": path,
            "comments": comments,
            "views": views,
            "likes": likes,
            "type": item_type
        }
