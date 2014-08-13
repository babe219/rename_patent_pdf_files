#!/usr/bin/env python
#-*-coding:utf-8 -*-
"""this script can rename patents downloading from 
<http://publicquery.sipo.gov.cn/index.jsp?language=zh_CN>.
pdfminer's tool: pdf2txt.py is the main methods

(1)for windows 7 and code is cp936.


"""
__version__ = "0.1"


import sys
import os 
import os.path
import re


def usage():
	print 'usage:%s pathway' % sys.argv[0]

if len(sys.argv) != 2:
	print usage()
	sys.exit(1)
elif os.path.exists(sys.argv[1]):
	os.chdir(sys.argv[1])
	filelist =  os.listdir(str(sys.argv[1]))
else:
	print "there is no this pathway ,plase input a new one!"
	sys.exit(1)

#get really pdf name and public NO.
def getpdfnameandno(fn):
	#set re pattern
	patterns1 = '申请公布日 (\d\d\d\d.\d\d.\d\d)CN'
	patterns2 = '发明名称(.*)\(\d\d\)摘要'
	
	pdfstr = os.popen("python C:\Python27\Scripts\pdf2txt.py -p 1 "+fn).read()
	pdfdate = re.search(patterns1, pdfstr).group(1).replace('.','_')
	pdfname = re.search(patterns2, pdfstr).group(1)
	return pdfdate, pdfname

def main():  
	for i in filelist:
		print i
		date, name =getpdfnameandno(i)
		newname = 'P%s_%s.pdf' %(date, name.decode('utf-8').encode('cp936'))
		print newname
		os.rename(i,newname)

if __name__ == '__main__':
	main()

