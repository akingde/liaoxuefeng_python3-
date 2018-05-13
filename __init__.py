# -*- coding:utf-8 -*-
# @author:lijinxi
# @file: __init__.py
# @time: 2018/05/07

import requests
from bs4 import BeautifulSoup
import pdfkit
import time
import os
import re
import  random


class Crawel(object):
    def __init__(self):
        self.htmlTemplate = '''
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
            </head>
            <body>
            {content}
            </body>
            </html>
'''
        # robots.txt不允许,设置请求头
        self.user_agent=[
            "Mozilla / 5.0(Windows NT 10.0;Win64; x64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 66.0.3359.139,Safari / 537.36",
            "Mozilla / 5.0(Windows NT 10.0;Win64; x64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 58.0.3029.110Safari / 537.36 Edge / 16.16299",
            " Mozilla / 5.0(WindowsNT10.0;WOW64;Trident / 7.0;LCTE;rv: 11.0) likeGecko",
            "Mozilla / 5.0(Windows NT 10.0;Win64;x64;rv: 59.0) Gecko / 20100101Firefox / 59.0",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER",
            "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; QQBrowser/7.0.3698.400)",
            "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
            "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)"
        ]
        self.headers = {
            "Proxy-Connection": "keep-alive",
            "Pragma": "no-cache",
            "Cache-Control": "no-cache",
            "User - Agent": str(self.user_agent[random.randint(0,len(self.user_agent)-1)]),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "DNT": "1",
            "Accept-Encoding": "gzip, deflate, sdch",
            "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.4",
            "Accept-Charset": "gb2312,gbk;q=0.7,utf-8;q=0.7,*;q=0.7",
            "Referer": "https: // www.liaoxuefeng.com /",
        }

    def getPageLinks(self):
        '''
        获取所有的URL集合
        :return:
        '''
        response = requests.get("https://www.liaoxuefeng.com/wiki/0014316089557264a6b348958f449949df42a6d3a2e542c000",
                                headers=self.headers)
        bsObj = BeautifulSoup(response.text, "lxml")
        menu_list = bsObj.find("ul", {"id": "x-wiki-index", "class": "uk-nav uk-nav-side"})
        pageLinks = []
        for pageLink in menu_list.findAll("a", {"class": "x-wiki-index-item"}):
            if pageLink.attrs["href"] is not None:
                newLink = "https://www.liaoxuefeng.com" + pageLink.attrs["href"]
                pageLinks.append(newLink)
        return pageLinks

    def getUrlContent(self, url, file):
        '''
        解析URL,获取HTML内容
        :param url:
        :param file:保存的html 文件名
        :return:
        '''
        response = requests.get(url, headers=self.headers)
        bsObj = BeautifulSoup(response.text, "lxml")
        # 正文
        pageContent = bsObj.find("div", {"class": "x-wiki-content x-main-content"})
        # 标题
        pageTitle = bsObj.find("h4").get_text()
        # 标题放在正文之前居中显示
        center_tag = bsObj.new_tag("center")
        title_tag = bsObj.new_tag("h1")
        title_tag.string = pageTitle
        center_tag.insert(1, title_tag)
        pageContent.insert(0, center_tag)
        html = str(pageContent)
        html = self.htmlTemplate.format(content=html)
        html = html.encode("utf-8")
        with open(file, 'wb+') as f:
            f.write(html)
        return file

    def sloveImage(self, filename1, filename2):
        '''
        解决图片不能正常保存的问题
        由路径引起,尝试修改路径
        :param filename1:原始文件
        :param filename2:修改后要保存的文件
        :return:
        '''
        with open(filename1, "rb+")  as f:
            text = f.read().decode("utf-8")
            text = text.replace("data-src", "src")
        with open(filename2, "wb+") as f:
            f.write(text.encode("utf-8"))
        return filename2

    def savePdf(self, htmls, filename):
        '''
        将所有的html保存到pdf文件
        :param htmls:
        :param filename:
        :return:
        '''
        options = {
            'page-size': 'Letter',
            'margin-top': '0.75in',
            'margin-right': '0.75in',
            'margin-bottom': '0.75in',
            'margin-left': '0.75in',
            'encoding': "UTF-8",
            'custom-header': [
                ('Accept-Encoding', 'gzip')
            ],
            'cookie': [
                ('cookie-name1', 'cookie-value1'),
                ('cookie-name2', 'cookie-value2'),
            ],
            'outline-depth': 10,
        }
        pdfkit.from_file(htmls, filename, options=options)


def main():
    '''
    处理
    :return:
    '''
    start = time.time()
    crawer = Crawel()
    filename = "liaoxuefeng_blogs_python3.pdf"
    pageLinks = crawer.getPageLinks()
    htmls = []  # html文件列表
    for index, pageLink in enumerate(pageLinks):
        if index<18:
            continue
        filename1 = "index" + str(index) + ".html"
        filename2 = "indexc" + str(index) + ".html"
        crawer.getUrlContent(pageLink, filename1)
        waittime=random.randint(0,20)+20;
        time.sleep(waittime)  # 给自己留一线生机
        html = crawer.sloveImage(filename1, filename2)
        htmls.append(html)
        print("第%d页采集完成........." % index)
    crawer.savePdf(htmls, filename)
    # 移除html文件
    ''''
    rex = re.compile("^index.*\.html$")
    for i in os.listdir():
        if rex.match(i):
            os.remove(i)
            '''
    total_time = time.time() - start
    print("总共运行了%d秒" % total_time)


if __name__ == '__main__':
    main()
