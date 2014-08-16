#!/usr/bin/env python
#-*-coding:utf-8 -*-
"""
this script can rename(example:P+publicdate+patentname) patents downloading from 
<http://publicquery.sipo.gov.cn/index.jsp?language=zh_CN>.
pdfminer's tool: pdf2txt.py is the main methods.this run successfully in windows7 .

Requirement；
(1)python 2
(2)pdf2txt.py of pdfminer

version 0.2 : impored feature
(1)add progress bar and complete percentage.
(2)add function to reduce wrongfiles.
(3)add comments about this script.

"""
__version__ = "0.2"


import sys
import os 
import os.path
import re


output = sys.stdout
errinfo = []
print "*"*30+'starting'+"*"*30

#deal with argument 
def usage():
	print 'usage:%s pathway' % sys.argv[0]

if len(sys.argv) != 2:
	print usage()
	sys.exit(1)
elif os.path.exists(sys.argv[1]):
	os.chdir(sys.argv[1])
	filelist =  os.listdir(str(sys.argv[1]))
	fileno = len(filelist)
	print "get pathway successful"
	print "get %d files from this pathway" %fileno
else:
	print "there is no this pathway ,plase input a new one!"
	sys.exit(1)

#get really pdf name and public NO.
def getpdfnameandno(fn):
	#set re pattern
	patterns1 = '申请公布日 (\d\d\d\d.\d\d.\d\d)CN'
	patterns2 = '发明名称(.*)\(\d\d\)摘要'
	
	pdfstr = os.popen("python pdf2txt.py -p 1 "+fn).read()
	pdfdate = re.search(patterns1, pdfstr).group(1).replace('.','_')
	pdfname = re.search(patterns2, pdfstr).group(1)
	return pdfdate, pdfname

def main():  
	
	for i in filelist:
		#setup percent 
		rate_num = 100*filelist.index(i)/int(fileno)
		output.write('\rcomplete percent %d %s\r'%(rate_num, '%') )
		output.flush()
		pattdownfile = "\d+[a-zA-Z]?.pdf"
		#deal wrong file
		if  not re.search(pattdownfile, i): 
			errinfo.append('%s : not patents or have renamed!' %i)
			pass
		else:
			date, name =getpdfnameandno(i)
			newname = 'P%s_%s.pdf' %(date, name)
			#print newname
			os.rename(i,newname)
	print "complete percent 100%"
	print "*"*20 + "rename all patents successful!!!" + "*"*20
	for i in errinfo:
		print '<'+ str(errinfo.index(i))+'>' + " "+ i
if __name__ == '__main__':
	main()

