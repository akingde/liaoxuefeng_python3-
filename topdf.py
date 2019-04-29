import pdfkit
import  os
import  re
def topdf(htmls,filename):
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
    '''
    toc = {
        'xsl-style-sheet': 'toc.xsl'
    }
    cover = 'cover.html'
    '''
    pdfkit.from_file(htmls, filename, options=options)

    #pdfkit.from_file('file.html', options=options, toc=toc, cover=cover, cover_first=True)

if __name__ == '__main__':
    htmls=[]
    for i in range(1,130):
        htmls.append('./html/'+str(i)+'-'+str(i)+'.html')
    print(htmls)
    num=1
    for i in htmls:
        filename='./pdf/'+str(num)+'.pdf'
        topdf(i,filename)
        num+=1
    #topdf(htmls,'liaoxuefeng-python3-v2.pdf')
    #htmls2=['1-1.html','2-2.html']
    #topdf(htmls2,'python3.pdf')    #加入script样式,不能一次成功,需合并
    #topdf('3.html','python03.pdf')
    '''
    rex=re.compile('^(\d+)\.html$')
    for i in os.listdir():
        if rex.match(i):
            htmls.append(i)
            print(i)
    #topdf(htmls,'python3.pdf')
    rex2=re.compile('^\d+')
    '''
    '''
    for i in os.listdir():
        if rex2.match(i):
            os.remove(i)
    '''