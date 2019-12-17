# -*-coding:utf-8-*-
# @author:lijinxi

import requests
from bs4 import BeautifulSoup
import time
import os
import pdfkit
import xlwt


class Crawl:
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome'
                      '/74.0.3729.28 Safari/537.36 OPR/61.0.3298.6 (Edition developer)',
    }

    templates = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title></title>
        {css}
        {js}
    </head>
    <body>
    {content}
    </body>
    </html>"""

    start_time = time.time()

    def __init__(self, start_url, pdf_to_save_name, css_save_path='./static/css/',
                 js_save_path='./static/js/',
                 pictures_save_path='./files/attachments/'):
        self.start_url = start_url
        self.pdf_to_save_name = pdf_to_save_name
        self.css_save_path = css_save_path
        self.picture_save_path = pictures_save_path
        self.contents = []
        self.css = []
        self.titles = []
        self.js = []

        if not os.path.exists(self.css_save_path):
            os.makedirs(self.css_save_path)

        self.start()

    def start(self):
        response = requests.get(self.start_url, headers=self.headers)
        bs_obj = BeautifulSoup(response.text, 'html5lib')
        bs_obj.declared_html_encoding = 'utf-8'
        menu = bs_obj.find('ul', {'id': 'x-wiki-index', 'class': 'uk-nav uk-nav-side'})
        head = bs_obj.find('head')
        styles = bs_obj.findAll('style')
        # internal css
        for style in styles:
            if style not in self.css:
                self.css.append(style)
        # save  external css
        stylesheet = head.findAll('link', {'rel': 'stylesheet'})
        if stylesheet is not None:
            for sheet in stylesheet:
                if sheet['href'] not in self.css:
                    res = requests.get('https://static.liaoxuefeng.com' + sheet['href'], sheet['href'])
                    if sheet['href'] == '/static/css/main.css?v=1.0-b1b83dc-2019-05-25T01:51:58Z':
                        sheet['href'] = '/static/css/main.css'
                    with open('.' + sheet['href'], 'w', encoding='utf-8') as f:
                        f.write(res.text)
                    sheet['href'] = '.' + sheet['href']
                    self.css.append(sheet)

        # external js
        javascripts = head.findAll('script', attrs={'src': True, 'async': False, 'charset': False})
        if javascripts is not None:
            for javascript in javascripts:
                if javascript['src'] not in self.css:
                    res = requests.get('https://static.liaoxuefeng.com' + javascript['src'], javascript['src'])
                    if not os.path.exists(os.path.dirname('.' + javascript['src'])):
                        os.makedirs(os.path.dirname('.' + javascript['src']))
                    if '?' in javascript['src']:
                        index = javascript['src'].index('?')
                        javascript['src'] = javascript['src'][:index]
                    with open('.' + javascript['src'], 'w', encoding='utf-8') as f:
                        f.write(res.text)
                    javascript['src'] = '.' + javascript['src']
                    self.js.append(javascript)

        for link in menu.findAll('a', {'class': 'x-wiki-index-item'}):
            if link.attrs['href'] is not None:
                absolute_link = 'https://www.liaoxuefeng.com' + link.attrs['href']
                self.get_content(absolute_link)
        self.xls()
        self.template_format()
        self.save_to_pdf()

    def get_content(self, url):
        print("正在抓取：{url}，当前耗时：{time}。".format(url=url, time=time.time() - self.start_time))
        try:
            response = requests.get(url, headers=self.headers)
            assert response.status_code == 200
        except AssertionError as e:
            print(e)
        except TimeoutError as e:
            print(e)
        except Exception as e:
            print(e)
        else:
            bs_obj = BeautifulSoup(response.text, 'html5lib')
            bs_obj.declared_html_encoding = 'utf-8'
            # handle content
            content = bs_obj.find('div', {'class': 'x-wiki-content x-main-content'})

            # delete video
            videos = bs_obj.findAll('iframe')
            if videos is not None:
                for video in videos:
                    video.extract()

            # save pictures
            pictures = content.find_all('img')
            for picture in pictures:
                real_url = picture.attrs['data-src']
                del picture.attrs['data-src']
                img = requests.get('https://static.liaoxuefeng.com' + real_url)
                dirname = os.path.dirname(real_url)
                if not os.path.exists('.' + dirname):
                    os.makedirs('.' + dirname)
                with open('.' + real_url + '.jpg', 'wb') as f:
                    f.write(img.content)
                picture.attrs['src'] = '.' + real_url + '.jpg'

            # save title
            title = bs_obj.find('h4').get_text()
            title_tag = bs_obj.new_tag('h1')
            title_tag.attrs['style'] = 'text-align:center'
            title_tag.string = title
            self.titles.append(title)
            self.contents.append(title_tag)
            self.contents.append(content)

            time.sleep(1)
            print("抓取完成，文章名为：{title}。".format(title=title))

    def save_to_pdf(self):
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

        toc = {
            'xsl-style-sheet': 'toc.xls'
        }
        '''
        cover = 'cover.html'
        '''
        pdfkit.from_file('templates.html', self.pdf_to_save_name, options=options)

        # pdfkit.from_file('file.html', options=options, toc=toc, cover=cover, cover_first=True)

    def xls(self):
        wb = xlwt.Workbook()
        ws = wb.add_sheet('目录')
        num = 0
        for title in self.titles:
            ws.write(num, 0, title.strip())
            num += 1
        wb.save('toc.xls')

    def template_format(self):
        with open('content.html', 'w', encoding='utf-8') as f:
            for content in self.contents:
                f.write(str(content))
        with open('css.html', 'w', encoding='utf-8') as f:
            for css in self.css:
                f.write(str(css))

        with open('js.html', 'w', encoding='utf-8') as f:
            for js in self.js:
                f.write(str(js))

        with open('content.html', 'r', encoding='utf-8') as f:
            content = f.read()
        with open('css.html', 'r', encoding='utf-8') as f:
            css = f.read()

        with open('js.html', 'r', encoding='utf-8') as f:
            js = f.read()

        html = self.templates.format(content=content, css=css, js=js)
        with open('templates.html', 'w', encoding='utf-8') as f:
            f.write(html)


if __name__ == '__main__':
    # crawl = Crawl("https://www.liaoxuefeng.com/wiki/1016959663602400/1019418790329088", 'liaoxuefeng_python3.pdf')
    # crawl = Crawl("https://www.liaoxuefeng.com/wiki/1252599548343744", 'liaoxuefeng_java12.pdf')
    # crawl = Crawl('https://www.liaoxuefeng.com/wiki/1022910821149312', 'liaoxuefeng_javascript.pdf')
    crawl = Crawl('https://www.liaoxuefeng.com/wiki/1177760294764384', 'liaoxuefeng_sql.pdf')
    # crawl=Crawl('https://www.liaoxuefeng.com/wiki/896043488029600','liaoxuefeng_git.pdf')
