#coding=gbk
'''
Created on 2013/06/28

@author: huxiufeng
'''

import os
import codecs
import re
import xlsHelper

class scanfile:
    def __init__(self,filename):
        self.fullname = filename
        (self.path1, self.names) = os.path.split(filename)
        (self.path0,self.paths) = os.path.split(self.path1)
    
    
    
    
    def getincludes(self):
        fd = codecs.open(self.fullname, 'r','gbk')
        self.includes = []
        reobj = re.compile(r'^\s*#include\s*"\S+"\s*')
        
        for lines in fd:
            #print lines
            match = reobj.search(lines)
            if match:
                includename = lines.split('"')[1]
                self.includes.append(includename)
        
        fd.close()
    
    def getfullfuncs(self):
        nBrace = 0
        nNote = 0
        
        fd = codecs.open(self.fullname, 'r','gbk')
        self.fullfuncs = []
        self.funcsdesc = []
        priline=''
        pridox = ''
        #reobj = re.compile(r'^[\s]*[\w]+[\s]+[\w]+\([[\w]*[\s]*[\w]*[\W]*]*\)\{[[\s]*[\S]*]*\}')
        for lines in fd:
            #print lines
            lines = str(lines).strip()
            if str(lines).startswith('//'):
                #print lines
                #priline = lines
                continue
            
            num = str(lines).find('//')
            if num >=0:
                lines = str(lines)[0:num-1]
                #print lines
            
            nNoteBeg = str(lines).count('/*')          
            nNote += nNoteBeg
            if nNoteBeg > 0:
                at = str(lines).find('/*')
                pridox = str(lines)[at+2:]
            if nNote > 0:
                nNoteEnd = str(lines).count('*/')
                if nNoteBeg >0 and nNoteEnd > 0:
                    at = str(pridox).find('*/')
                    pridox =str(pridox)[0:at]
                elif nNoteBeg >0 and nNoteEnd <=0:
                    pass
                elif nNoteEnd > 0:
                    at = str(lines).find('*/')
                    pridox += str(lines)[0:at]
                else:
                    pridox += str(lines)
                nNote -= nNoteEnd
                #priline = lines
                continue
            
            nBrace += str(lines).count('{')            
            if nBrace > 0:
                nBrace -= str(lines).count('}')
                #priline = lines
                continue
            
            if str(lines)=='' or str(lines).find('#') >= 0 or str(lines).find(';') >= 0:
                #priline = lines
                continue
            
            #print lines
            
            self.fullfuncs.append(lines)
            self.funcsdesc.append(pridox)
            #priline = lines
                    
        fd.close()
        self.netfuncs = []
        for func in self.fullfuncs:
            self.netfuncs.append(self.getfuncsname(func))

    def getfuncsname(self, func):
        num = str(func).find('(')
        pre = str(func)[0:num]
        funcname = pre.split()[-1].strip()
        if funcname.startswith('*'):
            funcname = funcname[1:]
        return funcname

    
    def getfuncpara(self,func):
        num1 = str(func).find('(')
        num2 = str(func).find(')')
        pre = str(func)[num1+1:num2-1]
        
        return pre.split(',')

    def getfuncret(self, func):
        num = str(func).find('(')
        pre = str(func)[0:num]
        pre = pre.strip()
        funcname = pre.split()[-1].strip()
        prefix = ''
        if funcname.startswith('*'):
            prefix = '*'
        num = str(pre).rfind(' ')       
        ret = str(pre)[0:num].strip()
        return ret+prefix
    
    def writetoxls(self,xlsfile):
        xls = xlsHelper.ExcelHelper(xlsfile)
        sheetnum = xls.getSheetCount()
        bsheetexist = False
        for i in range(sheetnum):
            xls.getSheet(i+1)
            sheetname = xls.GetSheetName()
            if sheetname == self.names :
                bsheetexist = True
                break
        if not bsheetexist:
            xls.newSheet(self.names)
            
        xls.activateSheet(self.names)
        for index in range(0, len(self.fullfuncs)):
            fullfunc = self.fullfuncs[index]
            funcdes = self.funcsdesc[index]
            xls.setCell(index+1, 1, self.getfuncsname(fullfunc))
            xls.setCell(index+1, 2, self.getfuncpara(fullfunc))
            xls.setCell(index+1, 3, self.getfuncret(fullfunc))
            xls.setCell(index+1, 4, funcdes)
        
        xls.save()
        xls.close()
        
#----------------------It is a split line--------------------------------------

def main():
    infile = r'F:\dwCheck.c'
    xlsfile = r'F:\work\20130108短信平台\6. 代码走查\doxgen\code.xlsx'
    scans = scanfile(infile)
    print scans.names
    print scans.paths
    scans.getincludes()
    print scans.includes
    scans.getfullfuncs()
    print scans.fullfuncs
    
    scans.writetoxls(xlsfile)
    
    for funcname in scans.fullfuncs:
        print scans.getfuncsname(funcname)
        print scans.getfuncpara(funcname)
        print scans.getfuncret(funcname)
    
#----------------------It is a split line--------------------------------------

if __name__ == "__main__":
    main()
    print "It's ok"