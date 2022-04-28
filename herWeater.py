# -*- coding: utf-8 -*-
# @Author  : ZXC
# @Time    : 2022/4/28 20:02
# @Function:
#!/usr/bin/python3
#coding=utf-8

import requests, json
import os
import requests
from bs4 import BeautifulSoup
import random
import os
import time
from lxml import etree
SCKEY=os.environ.get('SCKEY') ##Server酱推送KEY
def getIP():
    for i in range(1, 5):
        headers = {
            "User-Agent": UserAgent().chrome  # chrome浏览器随机代理
        }
        ip_url = 'http://www.xiladaili.com/gaoni/{}/'.format(i)
        html = requests.get(url=ip_url, headers=headers).text
        seletor = etree.HTML(html)
        ip_list = seletor.xpath('/html/body/div/div[3]/div[2]/table/tbody/tr/td[1]/text()')
        for i in range(len(ip_list)):
            ip = "http://" + ip_list[i]
            # 设置为字典格式
            proxies = {"http": ip}
            try:
                # 使用上面的IP代理请求百度，成功后状态码200
                baidu = requests.get("http://myip.ipip.net/", proxies=proxies,timeout=3)
                if baidu.status_code == 200:
                    print(proxies,baidu.text)
                    ips.append(proxies)
            except:
                print('错误')

        print("正在准备IP代理，请稍后。。。")
def getlovewords():
        # getIP()
    headers={
        'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Mobile Safari/537.36'
    }
    # 获取情话
    texts=[]
    for page in range(1,2):
        time.sleep(3)
        # proxy = ips[random.randint(0, len(ips) - 1)]
        # print(proxy)
        url = 'https://www.duanwenxue.com/huayu/tianyanmiyu/list_{}.html'.format(page)
        try:
            response = requests.get(url,headers=headers)
            soup=BeautifulSoup(response.text,'lxml')
            lovewordslist=soup.find('div',class_='list-short-article').find_all('a',target='_blank')
            # print(lovewordslist)
            texts.extend([lovewordslist[i].text for i in range(len(lovewordslist))])
        except:
            print("连接失败")
    if(len(texts)==0):
        print("情话集合为空")
        return
    else:
        todaywords = texts[random.randint(0, len(texts) - 1)]  # 随机选取其中一条情话
        return todaywords
def get_iciba_everyday():
    icbapi = 'http://open.iciba.com/dsapi/'
    eed = requests.get(icbapi)
    bee = eed.json()  #返回的数据
    english = bee['content']
    zh_CN = bee['note']
    str = '再说一次早安哦~\n'
    return str

def ServerPush(info): #Server酱推送
    api = "https://sc.ftqq.com/{}.send".format(SCKEY)
    title = u"美好的一天从睁开眼睛开始~"
    content = info.replace('\n', '\n\n')
    data = {
        "text": title,
        "desp": content
    }
    print(content)
    requests.post(api, data=data)
def main():
    try:
        api = 'http://t.weather.itboy.net/api/weather/city/'             #API地址，必须配合城市代码使用
        city_code = '101220101'   #进入https://where.heweather.com/index.html查询你的城市代码
        tqurl = api + city_code
        response = requests.get(tqurl)
        d = response.json()         #将数据以json形式返回，这个d就是返回的json数据
        if(d['status'] == 200):     #当返回状态码为200，输出天气状况
            parent = d["cityInfo"]["parent"] #省
            city = d["cityInfo"]["city"] #市
            update_time = d["time"] #更新时间
            date = d["data"]["forecast"][0]["ymd"] #日期
            week = d["data"]["forecast"][0]["week"] #星期
            weather_type = d["data"]["forecast"][0]["type"] # 天气
            wendu_high = d["data"]["forecast"][0]["high"] #最高温度
            wendu_low = d["data"]["forecast"][0]["low"] #最低温度
            shidu = d["data"]["shidu"] #湿度
            pm25 = str(d["data"]["pm25"]) #PM2.5
            pm10 = str(d["data"]["pm10"]) #PM10
            quality = d["data"]["quality"] #天气质量
            fx = d["data"]["forecast"][0]["fx"] #风向
            fl = d["data"]["forecast"][0]["fl"] #风力
            ganmao = d["data"]["ganmao"] #感冒指数
            tips = d["data"]["forecast"][0]["notice"] #温馨提示
            # 天气提示内容

            wendu1 = wendu_high
            if wendu1 <= "高温 -15℃":
                chuanyizhishu = '天气寒冷，冬季着装：棉衣、羽绒服、冬大衣、皮夹克加羊毛衫、厚呢外套、呢帽、手套等；年老体弱者尽量少外出'
            if "高温 -15℃" < wendu1 <= "高温 5℃":
                chuanyizhishu = '天气冷，冬季着装：棉衣、羽绒衣、冬大衣、皮夹克、毛衣再外罩大衣等；年老体弱者尤其要注意保暖防冻'
            if "高温 5℃" < wendu1 <= "高温 15℃":
                chuanyizhishu = '天气凉，适宜着一到两件羊毛衫、大衣、毛套装、皮夹克等春秋着装；年老体弱者宜着大衣、夹衣或风衣加羊毛衫等厚型春秋着装'
            if "高温 15℃" < wendu1 <= "高温 20℃":
                chuanyizhishu = '天气温凉，适宜着夹衣、马甲衬衫、长裤、夹克衫、西服套装加薄羊毛衫等春秋服装。年老体弱者：夹衣或风衣加羊毛衫'
            if "高温 20℃" < wendu1 <= "高温 25℃":
                chuanyizhishu = '天气暖和，适宜着单层棉麻面料的短套装、T恤衫、薄牛仔衫裤、休闲服、职业套装等春秋过渡装。年老体弱者请适当增减衣服'
            if "高温 25℃" < wendu1 <= "高温 28℃":
                chuanyizhishu = '天气偏热，适宜着短衫、短裙、短套装、T恤等夏季服装。年老体弱者：单层薄衫裤、薄型棉衫'
            if "高温 28℃" < wendu1 <= "高温 33℃":
                chuanyizhishu = '天气炎热，适宜着短衫、短裙、短裤、薄型T恤衫、敞领短袖棉衫等夏季服装'
            if "高温 33℃" < wendu1:
                chuanyizhishu = '天气极热，适宜着丝麻、轻棉织物制作的短衣、短裙、薄短裙、短裤等夏季服装。午后尽量减少户外活动，高温条件下作业和露天作业人员采取必要防护措施'
            tdwt = "宝贝早安！\n今天天气怎么样呢？\n宝贝在哪： " + parent + city + \
                   "\n日期： " + date + "\n星期: " + week + "\n今天天气: " + weather_type + "\n温度: " + wendu_high + " / "+ wendu_low + "\n湿度: " + \
                    shidu + "\nPM25: " + pm25 + "\nPM10: " + pm10 + "\n空气质量: " + quality + \
                   "\n风力风向: " + fx + fl + "\n感冒指数: " + ganmao + "\n穿衣建议: " + chuanyizhishu  + "\n爱你哦： " + tips + "\n更新时间: " + update_time + "\n✁-----------------------------------------\n" + get_iciba_everyday()
            # print(tdwt)


            # requests.post(cpurl,tdwt.encode('utf-8'))         #把天气数据转换成UTF-8格式，不然要报错。
            ServerPush(tdwt)
            # CoolPush(tdwt)
    except Exception:
        error = '【出现错误】\n　　今日天气推送错误，请检查服务或网络状态！'
        print(error)
        print(Exception)

if __name__ == '__main__':
    main()
    print("hello")
