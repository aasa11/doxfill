#coding=gbk
'''
Created on 2013/06/28

@author: huxiufeng
'''

class doxpara:
    def __init__(self):
        pass

    def getdoxfile(self, filename, pathname, sec1, sec2, funcs, includes):
        dox = '''
/** @file
\t@brief  ԭ�Ӳ�����

\t@ingroup '''
        dox += str(pathname)
        dox += '''
        '''
        dox += '\n\t@section sec' + str(sec1) + '_' + str(sec2) + '_1     ' + str(sec1) + '.' + str(sec2) + '.1 ����˵��\n'
        for names in funcs:
            dox += '\t  @li ' + str(names) + '\n'
        
        dox += '\n\n'
        dox += '\t@section sec' + str(sec1) + '_' + str(sec2) + '_2     ' + str(sec1) + '.' + str(sec2) + '.2 ����˵��\n'        
        for names in includes:
            dox += '\t  @li ' + str(names) + '\n'
            
        dox += '\n\n'
        dox += '\t@section sec' + str(sec1) + '_' + str(sec2) + '_3     ' + str(sec1) + '.' + str(sec2) + '.3 �ؼ��������ڲ��ṹ����\n'        
       
        dox += '''\t   ��

\t@author xfhu
*/
        '''
        return dox
        
    
    def getdoxfunc(self, func, paras, rets):
        dox = '/** @brief  '+str(func)+'\n\n'
        
        dox += '\t     @par ��������: '+'\n\n'
        dox += '\t@param\n'
        for names in paras:
            dox += '\t  '+str(names)+'\n'
            
        dox+='\n\n'
        dox+='\t@return : ' +str(rets)+ '\n'
        if str(rets).find('int')>=0 :
            dox +=  '\t  @ret 0  �ɹ�\n\t  @ret -1  ʧ��\n\n'
        elif str(rets).find('void')>=0 :
            dox += '\t @ret ��\n\n'
        else :
            dox += '\t  @ret \n\n'
            
        dox +='''
      @par �㷨����: 
        @li ��

      @par �ؼ��������ڲ��ṹ����:
        @li ��

      @par ������������:
        @li ��        

      @par ���ݿ��ʹ�ã�
        @li ��

      @par�ļ�ʹ�ã�
        @li ��

      @par IPCʹ�ã�
        @li ��

      @exception
        @li �������ʧ��

*/
'''    
        

        return dox

#----------------------It is a split line--------------------------------------

def main():
    filename = 'file1'
    pathname = 'path1'
    sec1 = 9
    sec2 = 10
    funcs = ["fun1", "func2", "func3"]
    includes = ["include1", "inl2", "inl3"]
    dox = doxpara()
    print dox.getdoxfile(filename, pathname, sec1, sec2, funcs, includes)
    
    func = "funcs1"
    paras = ["void ba","int cd"]
    rets = 'int'
    print dox.getdoxfunc(func, paras, rets)
    
#----------------------It is a split line--------------------------------------

if __name__ == "__main__":
    main()
    print "It's ok"
