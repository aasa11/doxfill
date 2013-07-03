#coding=GBK
'''
Created on 2013/07/01

@author: huxiufeng
'''

import writedox
import scanfile
import codecs
import os
import xlsHelper

class funcdoc:
    def __init__(self):
        self.file = ''
        self.name = ''
        self.para = ''
        self.ret = ''
        self.desc = ''
        self.proc = ''
        self.db = ''
        
    def __str__(self):
        strout =  "file: "+self.file +  "\n" + \
                "name: "+self.name +  "\n" +    \
                "para: "+self.para +  "\n" +    \
                "ret: "+self.ret +  "\n" +  \
                "desc: "+self.desc +  "\n" +    \
                "proc: "+self.proc +  "\n" +    \
                "db: "+self.db +  "\n" +    \
                "\n"
        return strout
        
    

class batchop:
    def __init__(self):
        pass
    
    def batchwrtiexls(self,parafile, xlsfile):
        paras = codecs.open(parafile, 'r')
        if not os.path.exists(xlsfile):
            print "not exist file: "+xlsfile
            return
        xls = xlsHelper.ExcelHelper(xlsfile)
        for lines in paras:
            [filename, _] = lines.split(',')
            #netfilename = os.path.split(filename)[-1]
            sc = scanfile.scanfile(filename)
            sc.getincludes()
            sc.getfullfuncs()
            sheetnum = xls.getSheetCount()
            bsheetexist = False
            for i in range(sheetnum):
                xls.getSheet(i+1)
                sheetname = xls.GetSheetName()
                if sheetname == sc.names :
                    bsheetexist = True
                    break
            if not bsheetexist:
                xls.newSheet(sc.names)
            else:
                xls.activateSheet(sc.names)
                
                
            xls.activateSheet(sc.names)
            
            xls.setCell(1, 1, r'函数名')
            xls.setCell(1, 2, r'函数参数')
            xls.setCell(1, 3, r'函数返回值')
            xls.setCell(1, 4, r'函数描述')
            xls.setCell(1, 5, r'函数过程')
            xls.setCell(1, 6, r'数据库表')
            
            for index in range(0, len(sc.fullfuncs)):
                fullfunc = sc.fullfuncs[index]
                funcdes = sc.funcsdesc[index]
                xls.setCell(index+2, 1, sc.getfuncsname(fullfunc))
                xls.setCell(index+2, 2, sc.getfuncpara(fullfunc))
                xls.setCell(index+2, 3, sc.getfuncret(fullfunc))
                xls.setCell(index+2, 4, funcdes)
        
        xls.save()
        xls.close()
        
    def batchreadxls(self, xlsfile):
        self.funcsdes = {}
        
        if not os.path.exists(xlsfile):
            print "not exist file: "+xlsfile
            return
        xls = xlsHelper.ExcelHelper(xlsfile)
        sheetnum = xls.getSheetCount()
        for i in range(sheetnum):
            xls.getSheet(i+1)
            sheetname = xls.GetSheetName()
            xls.activateSheet(sheetname)
            col = xls.GetUsedRowsNum()
            for index in range(1,col+1):
                funcname = xls.getCell(index,1)
                if str(funcname) == '' or funcname == None:
                    break
                des = funcdoc()
                des.file = sheetname
                des.name = str(funcname)
                des.para = str(xls.getCell(index,2))
                des.ret = str(xls.getCell(index,3))
                des.desc = str(xls.getCell(index,4))
                des.proc = str(xls.getCell(index,5))
                des.db = str(xls.getCell(index,6))
                if self.funcsdes.has_key(des.file):
                    value = self.funcsdes[des.file]
                    value[des.name]=des
                else:
                    value = {}
                    value[des.name]=des
                    self.funcsdes[des.file]=value
        
        xls.close()
        
    def writedox(self, parafile, xlsfile, outpath):
        self.batchreadxls(xlsfile)
        for (_,v1) in self.funcsdes.items():
            for (_,v) in v1.items():
                print v
        
        paras = codecs.open(parafile, 'r')
        for lines in paras:
            [filename, sec] = lines.split(',')
            netfilename = os.path.split(filename)[-1]
            outfile = os.path.join(outpath,netfilename)
            print outfile
            [sec1,sec2]=str(sec).strip().split('.')
            wd = writedox.writedoxfuncs(filename, outfile, sec1, sec2, self.funcsdes)
            wd.write()
            
        

#----------------------It is a split line--------------------------------------

def main():
    parafile = 'F:/dox/dox.txt'
    paras = codecs.open(parafile, 'r')
    for lines in paras:
        [filename, sec] = lines.split(',')
        netfilename = os.path.split(filename)[-1]
        outfile = 'F:/dox/data/'+netfilename
        [sec1,sec2]=str(sec).strip().split('.')
        wd = writedox.writedox(filename, outfile, sec1, sec2)
        wd.write()


def main1():
    parafile = r'F:\work\20130108短信平台\6. 代码走查\doxgen\dox.txt'
    xlsfile = r'F:\work\20130108短信平台\6. 代码走查\doxgen\code.xlsx'
    paras = codecs.open(parafile, 'r')
    for lines in paras:
        [filename, sec] = lines.split(',')
        netfilename = os.path.split(filename)[-1]
        sc = scanfile.scanfile(filename)
        sc.getincludes()
        sc.getfullfuncs()
        sc.writetoxls(xlsfile)
        
def main_genxls():
    parafile = r'F:\work\20130108短信平台\6. 代码走查\doxgen\dox.txt'
    xlsfile = r'F:\work\20130108短信平台\6. 代码走查\doxgen\code.xlsx'
    bo = batchop()
    bo.batchwrtiexls(parafile, xlsfile)
    
def main3():
    xlsfile = r'F:\work\20130108短信平台\6. 代码走查\doxgen\code.xlsx'
    bo = batchop()
    bo.batchreadxls(xlsfile)
    for (_,v1) in bo.funcsdes.items():
        for (_,v) in v1.items():
            print v
            

def main_gencode():
    parafile = r'F:\work\20130108短信平台\6. 代码走查\doxgen\dox.txt'
    xlsfile = r'F:\work\20130108短信平台\6. 代码走查\doxgen\code.xlsx'
    outpath = r'F:\work\20130108短信平台\6. 代码走查\doxgen\data'
    bo = batchop()
    bo.writedox(parafile, xlsfile, outpath)
    
    
#----------------------It is a split line--------------------------------------

if __name__ == "__main__":
    #main()
    main_gencode()
    print "It's ok"