#-*-coding:utf-8-*-
#@author:lijinxi
'''
generate xls
'''
import xlwt
import  xlrd
def txttoxls(src,dst):
    with open(src,'r') as f:
        wb = xlwt.Workbook()
        ws = wb.add_sheet('目录')
        num=0
        for i in f:
            i=i.strip()
            ws.write(num,0,i)
            num+=1
        wb.save(dst)

txttoxls('url.txt','toc.xls')
