#coding=GBK
'''
Created on 2013/07/01

@author: huxiufeng
'''

import codecs
import doxpara
import scanfile

class writedoxfuncs:
        def __init__(self, infile, outfile, sec1, sec2, funcsdes):
            self.infile = infile
            self.outfile = outfile
            self.sec1 = sec1
            self.sec2 = sec2 
            self.funcsdes = funcsdes
            self.sc = scanfile.scanfile(self.infile)
            self.sc.getincludes()
            self.sc.getfullfuncs()
            
            
        def getdoxfile(self):
            dox = '''
/** @file
    @brief  ԭ�Ӳ�����

    @ingroup '''
            dox += str(self.sc.paths)
            dox += '''
            '''
            dox += '\n    @section sec' + str(self.sec1) + '_' + str(self.sec2) + '_1     ' + str(self.sec1) + '.' + str(self.sec2) + '.1 ����˵��\n'
            if not self.funcsdes.has_key(self.sc.names):
                print "no file : "+self.sc.names
                return
            funcpage = self.funcsdes[self.sc.names]
            for (_,funcs) in funcpage.items():
                dox += '      @li ' + str(funcs.name) + '         '+str(funcs.desc)+'\n'
            
            dox += '\n\n'
            dox += '    @section sec' + str(self.sec1) + '_' + str(self.sec2) + '_2     ' + str(self.sec1) + '.' + str(self.sec2) + '.2 ����˵��\n'        
            for names in self.sc.includes:
                dox += '      @li ' + str(names) + '\n'
                
            dox += '\n\n'
            dox += '    @section sec' + str(self.sec1) + '_' + str(self.sec2) + '_3     ' + str(self.sec1) + '.' + str(self.sec2) + '.3 �ؼ��������ڲ��ṹ����\n'        
           
            dox += '''       ��
    
    @author xfhu
*/
            '''
            return dox
        
        def getdoxfunc(self,funcname):
            if not self.funcsdes.has_key(self.sc.names):
                print "no file: "+self.sc.names
                return
            funcs = self.funcsdes[self.sc.names]
            if not funcs.has_key(funcname):
                print "no funcs: "+ funcname
                return
            funcdoc = funcs[funcname]
        
            dox = '/** @brief  '+str(funcdoc.name)+'\n\n'
            
            dox += '    @par ��������: '+'\n              '+ funcdoc.desc+'\n'
            
            dox += '\n    @param\n'
            paras = funcdoc.para.split(',')
            for names in paras:
                dox += '      '+str(names)+'\n'
                
            dox+='\n\n'
            dox+='    @return : ' +str(funcdoc.ret)+ '\n'
            if str(funcdoc.ret).find('int')>=0 :
                dox +=  '      @ret 0  �ɹ�\n      @ret -1  ʧ��\n\n'
            elif str(funcdoc.ret).find('void')>=0 :
                dox += '      @ret ��\n\n'
            else :
                dox += '      @ret \n\n'
                
            dox +='''
    @par �㷨����: 
        @li '''
            if funcdoc.proc == '' or funcdoc.proc is None:
                dox += '��'
            else :
                dox += funcdoc.proc

            dox +='''
    
    @par �ؼ��������ڲ��ṹ����:
      @li ��

    @par ������������:
      @li ��        

    @par ���ݿ��ʹ�ã�
      @li '''
            if funcdoc.db == '' or funcdoc.db is None:
                dox += '��'
            else :
                dox += funcdoc.db
            dox +='''
    
    @par�ļ�ʹ�ã�
      @li ��

    @par IPCʹ�ã�
      @li ��

    @exception
      @li �������ʧ��

*/
'''    
            
    
            return dox            
            
        def write(self):
            outfile = codecs.open(self.outfile, 'w', 'gbk')
            infile  = codecs.open(self.infile, 'r', 'gbk')
            
            sc = scanfile.scanfile(self.infile)
            dox = doxpara.doxpara()
            sc.getincludes()
            sc.getfullfuncs()
            
            nBrace = 0
            nNote = 0
            
            ishead = 0
            
            for lines in infile:
                if str(lines).find('//') >= 0:
                    outfile.write(lines)
                    continue
                
                nNote += str(lines).count('/*')
                if nNote > 0:
                    outfile.write(lines)
                    nright = str(lines).count('*/')
                    nNote -= nright
                    
                    if ishead == 0 and nright > 0: #add file comment
                        ishead = 1
                        filecomment = self.getdoxfile()
                        outfile.write(filecomment)           
                    continue
                
                nBrace += str(lines).count('{')
                if nBrace > 0:
                    outfile.write(lines)
                    nright = str(lines).count('}')
                    nBrace -= nright
                    continue
                
                
                newline = lines.strip()
                if str(newline) =='' or str(newline).find(';')>=0 or str(newline).find('#')>=0:
                    outfile.write(lines)
                    print lines
                    continue
                
                #add func comment
                #print lines
                funcname = str(lines).strip()
                funccomment = self.getdoxfunc(self.sc.getfuncsname(funcname))
                outfile.write(funccomment)
                outfile.write(lines)


                
            
#----------------------It is a split line--------------------------------------
class writedox:
    def __init__(self, infile, outfile, sec1, sec2):
        self.infile = infile
        self.outfile = outfile
        self.sec1 = sec1
        self.sec2 = sec2
        
    def write(self):
        outfile = codecs.open(self.outfile, 'w', 'gbk')
        infile  = codecs.open(self.infile, 'r', 'gbk')
        
        sc = scanfile.scanfile(self.infile)
        dox = doxpara.doxpara()
        sc.getincludes()
        sc.getfullfuncs()
        
        nBrace = 0
        nNote = 0
        
        ishead = 0
        
        for lines in infile:
            if str(lines).find('//') >= 0:
                outfile.write(lines)
                continue
            
            nNote += str(lines).count('/*')
            if nNote > 0:
                outfile.write(lines)
                nright = str(lines).count('*/')
                nNote -= nright
                
                if ishead == 0 and nright > 0: #add file comment
                    ishead = 1
                    filecomment = dox.getdoxfile(sc.names, sc.paths, self.sec1, self.sec2, sc.netfuncs, sc.includes)
                    outfile.write(filecomment)           
                continue
            
            nBrace += str(lines).count('{')
            if nBrace > 0:
                outfile.write(lines)
                nright = str(lines).count('}')
                nBrace -= nright
                continue
            
            
            newline = lines.strip()
            if str(newline) =='' or str(newline).find(';')>=0 or str(newline).find('#')>=0:
                outfile.write(lines)
                print lines
                continue
            
            #add func comment
            #print lines
            funcname = str(lines).strip()
            funccomment = dox.getdoxfunc(sc.getfuncsname(funcname), sc.getfuncpara(funcname), sc.getfuncret(funcname))
            outfile.write(funccomment)
            outfile.write(lines)
                
            
#----------------------It is a split line--------------------------------------

def main():
    infile = 'F:/Code/ecprj/zsms/src/dwproc/dwCheck.c'
    outfile = 'F:/Code/ecprj/zsms/src/dwproc/dwCheck.c.bak'
    wd = writedox(infile, outfile, 1, 2)
    wd.write()
    
#----------------------It is a split line--------------------------------------

if __name__ == "__main__":
    main()
    print "It's ok"