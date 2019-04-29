#--coding:utf-8--
#@author:lijinxi
'''
move file
'''
import os
import  shutil

def mvfile(ext,path):
    for file in os.listdir('.'):
        #fpath,fname=os.path.split()
        if file.endswith(ext):
            shutil.move(file,path+file)
if __name__ == '__main__':
    #mvfile('.html','./htmls/')
    #mvfile('.pdf','./pdfs/')
    mvfile('.jpg','./pictures/')
