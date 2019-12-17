# -*-coding:utf-8-*-
# @author:lijinxi

# 合并多个pdf文件
import os
from argparse import ArgumentParser, RawTextHelpFormatter
from PyPDF2 import PdfFileReader, PdfFileWriter


def mergepdf(outfile):
    pdflist = []
    for i in range(1, 130):
        pdflist.append(str(i) + '.pdf')
    print(pdflist)
    '''
    for p in os.listdir(path):
        if p.endswith('pdf'):
            pdflist.append()
    '''
    out = PdfFileWriter()
    outpages = 0
    for pdf in pdflist:
        fin = PdfFileReader(open(pdf, 'rb'))
        pageCount = fin.getNumPages()
        title = fin.getDocumentInfo()['/Title'].replace(' - 廖雪峰的官方网站', '')  # 添加书签信息
        print(title)
        outpages += pageCount
        print("页数：%d" % pageCount)
        for i in range(pageCount):
            out.addPage(fin.getPage(i))
        out.addBookmark(title=title, pagenum=outpages - pageCount)
    print('总页数：%d' % outpages)
    fout = open(outfile, 'wb')
    out.write(fout)
    fout.close()


mergepdf("liaoxuefeng_python3.pdf")
