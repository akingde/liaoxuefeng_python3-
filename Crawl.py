#--coding:utf-8--
#@author:lijinxi
'''
获取所有urls
'''
import  requests
from  bs4 import  BeautifulSoup

url=r'https://www.liaoxuefeng.com/wiki/0014316089557264a6b348958f449949df42a6d3a2e542c000'
header={
    'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'
}
response=requests.get(url,headers=header)
bsObj=BeautifulSoup(response.text,'html5lib')
menu=bsObj.find('ul',{'id':'x-wiki-index','class':'uk-nav uk-nav-side'})
num=0
with open('url.txt','w') as f:
    for link in menu.findAll('a',{'class':'x-wiki-index-item'}):
        num+=1;
        if link.attrs['href'] is not None:
            absolutelink='https://www.liaoxuefeng.com'+link.attrs['href']
            #absolutelink.encode('utf-8')
            f.write(absolutelink+'\n')
print('%d urls '%num);