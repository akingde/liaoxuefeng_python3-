#--coding:utf-8--
#@author:lijinxi
'''
解析url并保存为html
'''
import  requests
from bs4 import  BeautifulSoup
import  time
header={
    'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'
}
#url=r'https://www.liaoxuefeng.com/wiki/0014316089557264a6b348958f449949df42a6d3a2e542c000'
htmlTemplate = '''
<!DOCTYPE html>
<html lang="en">
    {head}
    <body>
    {content}
    </body>
</html>'''
def getcontent(url,htmlfilenum):
    respones=requests.get(url,headers=header)
    print(respones)
    bsObj=BeautifulSoup(respones.text,'html5lib')
    head=bsObj.find('head')
    errscript1=head.find('script',{'src':'//pagead2.googlesyndication.com/pagead/js/adsbygoogle.js'})
    errscript2=head.findAll('script')[-1]
    #print(errscript1,errscript2)
    errscript1.extract()
    errscript2.extract()
    content=bsObj.find('div',{'class':'x-wiki-content x-main-content'})
    pictures=content.find_all('img')
    pic_num=0;
    for pic in pictures:
        pic_num+=1
        reurl=pic.attrs['data-src']
        del pic.attrs['data-src']
        img=requests.get(reurl)
        pic_filename='./pictures/'+str(htmlfilenum)+'-'+str(pic_num)+'.jpg'
        with open(pic_filename,'wb') as f:
            f.write(img.content)
        pic.attrs['src']=pic_filename
    title=bsObj.find('h4').get_text()
    title_tag=bsObj.new_tag('h1')
    title_tag.attrs['style']='text-align:center'
    title_tag.string = title
    content.insert(0, title_tag)
    html=htmlTemplate.format(head=head,content=content)
    #html=htmlTemplate.format(content=content)
    #htmlfilename=str(htmlfilenum)+'.html'
    htmlfilename = './html/'+str(htmlfilenum)+'-'+str(htmlfilenum) + '.html'
    with open(htmlfilename,'w',encoding='utf-8') as f:
        f.write(html)
    print(htmlfilenum,"Done")

if __name__ == '__main__':
    htmlfilenum=0
    #urls=[]
    #getcontent('https://www.liaoxuefeng.com/wiki/0014316089557264a6b348958f449949df42a6d3a2e542c000/001431611988455689d4c116b2c4ed6aec000776c00ed52000',5)
    #getcontent('https://www.liaoxuefeng.com/wiki/0014316089557264a6b348958f449949df42a6d3a2e542c000/001431608990315a01b575e2ab041168ff0df194698afac000',2)
    with open('url.txt','r') as f:
        for url in f:
            htmlfilenum += 1
            getcontent(url.strip(),htmlfilenum)
            time.sleep(12)
            #urls.append(url.strip())      #必须去掉\n换行
            #getcontent(url,htmlfilenum)
            #time.sleep(60)




