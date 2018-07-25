# -*- coding: utf-8 -*-

import requests
import urllib
import re
from bs4 import BeautifulSoup


class Yahoo_api():

    def __init__(self, keyword):
        url = "https://shopping.yahooapis.jp/ShoppingWebService/V1/json/itemSearch"

        payload = {
            'appid': ['dj00aiZpPUlWT2MxZHJZNzlPMiZzPWNvbnN1bWVyc2VjcmV0Jng9M2U-'],
            'query': keyword,
            'hits': 20,
            # 'sort': '+itemPrice',
        }

        r = requests.get(url, params=payload)
        resp = r.json()

        item_list = resp["ResultSet"]["0"]["Result"]
        totalhit = int(resp['ResultSet']['totalResultsReturned'])

        image = [item_list[str(hit)]['Image']['Medium'] for hit in range(totalhit)]
        name = [item_list[str(hit)]['Name'] for hit in range(totalhit)]
        urls = [item_list[str(hit)]['Url'] for hit in range(totalhit)]
        price = ["{:,}".format(int(item_list[str(hit)]['Price']['_value'])) + '円' for hit in range(totalhit)]
        review = ['★-' if float(item_list[str(hit)]['Review']['Rate'])==0 else '★'+ str(item_list[str(hit)]['Review']['Rate']) for hit in range(totalhit)]
        review_count = ['(-件) ' if int(item_list[str(hit)]['Review']['Count'])==0 else '('+str(item_list[str(hit)]['Review']['Count'])+'件) ' for hit in range(totalhit)]

        keys = ('image', 'name', 'url', 'price', 'review', 'review_count')
        content = (image, name, urls, price, review, review_count)
        content_dict = dict(zip(keys,content))

        self.res = {}
        for i in range(len(name)):
            for v in range(len(keys)):
                code = keys[v] + str(i) + 'y'
                self.res[code] = content_dict[keys[v]][i]


class Rakuten_api():

    def __init__(self, keyword):
        url = 'https://app.rakuten.co.jp/services/api/IchibaItem/Search/20140222'

        payload = {
            'applicationId': ['1065001390664427204'],
            'keyword': keyword,
            'hits': 20,
            'sort': 'standard',
        }

        r = requests.get(url, params=payload)
        resp = r.json()

        item = [i['Item'] for i in resp['Items']]
        imageFlag = [i['imageFlag'] for i in item]
        image = []
        count=0
        for flag in imageFlag:
            if flag:
                image.append(item[count]['mediumImageUrls'][0]['imageUrl'])
            else:
                image.append('../../static/image/noimage.png')
            count+=1

        name = [i['itemName'] for i in item]
        urls = [i['itemUrl'] for i in item]
        price = ["{:,}".format(int(i['itemPrice'])) + '円' for i in item]
        review = ['★-' if float(i['reviewAverage'])==0 else '★'+str(i['reviewAverage']) for i in item]
        review_count = ['(-件) ' if int(i['reviewCount'])==0 else '('+str(i['reviewCount'])+'件) ' for i in item]

        keys = ('image', 'name', 'url', 'price', 'review', 'review_count')
        content = (image, name, urls, price, review, review_count)
        content_dict = dict(zip(keys,content))

        self.res = {}
        for i in range(len(name)):
            for v in range(len(keys)):
                code = keys[v] + str(i) + 'r'
                self.res[code] = content_dict[keys[v]][i]

class Amazon_html():

    def __init__(self, keyword):
        base_url = "https://www.amazon.co.jp/s/ref=nb_sb_noss_2?__mk_ja_JP=%E3%82%AB%E3%82%BF%E3%82%AB%E3%83%8A&url=search-alias%3Daps&field-keywords="
        book_url = 'https://www.amazon.co.jp/s/ref=nb_sb_noss_1?__mk_ja_JP=%E3%82%AB%E3%82%BF%E3%82%AB%E3%83%8A&url=search-alias%3Dstripbooks&field-keywords='

        if keyword == '本' :
            url = book_url + urllib.parse.quote(keyword)
        else :
            url = base_url + urllib.parse.quote(keyword)

        data = urllib.request.urlopen(url)

        # HTMLの取得
        html = data.read().decode('utf-8')

        # html 全体に対して操作
        itemResultlist = re.findall('<li id="result_[0-9+].*' , html)

        image = []
        name = []
        urls = []
        price = []
        review = []
        review_count = []

        # 検索結果アイテム1つに対して操作
        if itemResultlist:
            if '<!-- Product' in itemResultlist[0] :
                del itemResultlist[0]   # result_0 の消去
            for itemResult in itemResultlist:

                soup = BeautifulSoup(itemResult, "html.parser")

                # タイトルの抽出
                title = [a.get("title") for a in soup.find_all("a")]
                title = [x for x in title if x]
                name.append(title[0])

                # 詳細URLの取得
                urls.extend([a.get("href") for a in soup.find_all("a",limit=1)])

                # 画像URLの取得
                img = soup.find_all("img", limit=1)
                for l in img:
                    image.append(l['src'])

                # 価格の収録
                prc = re.findall('￥ [0-9]+[,]?[0-9]+' , itemResult)
                if not prc :
                    price.append('0')
                else :
                    price.append(prc[0].replace('￥ ', ''))

                asin = [a.get("name") for a in soup.find_all("span")]
                asin = [x for x in asin if x]
                if not asin :
                    item_asin = 'XXXXXXXXXX'
                else :
                    item_asin = asin[0]

                #base_str = '<span class="a-declarative" data-action="a-popover" data-a-popover="{&quot;max-width&quot;:&quot;700&quot;,&quot;closeButton&quot;:&quot;false&quot;,&quot;position&quot;:&quot;triggerBottom&quot;,&quot;url&quot;:&quot;/review/widgets/average-customer-review/popover/ref=acr_search__popover?ie=UTF8&amp;asin='
                base_str = 'asin='
                search_str = base_str + item_asin + r'.*'

                m = re.search(search_str, html)

                if m is not None :
                    rev = re.findall('(\d*[.,]?\d)</span>' , m.group(0))
                    review.append('★'+str(rev[0]))
                else :
                    review.append('★-')

                review_count.append('(-件) ')


        # HTMLファイルを閉じる
        price = [i + '円' for i in price]
        data.close()

        keys = ('image', 'name', 'url', 'price', 'review', 'review_count')
        content = (image, name, urls, price, review, review_count)
        content_dict = dict(zip(keys,content))

        self.res = {}
        for i in range(len(name)):
            for v in range(len(keys)):
                code = keys[v] + str(i) + 'a'
                self.res[code] = content_dict[keys[v]][i]