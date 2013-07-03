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
\t@brief  原子操作：

\t@ingroup '''
        dox += str(pathname)
        dox += '''
        '''
        dox += '\n\t@section sec' + str(sec1) + '_' + str(sec2) + '_1     ' + str(sec1) + '.' + str(sec2) + '.1 程序说明\n'
        for names in funcs:
            dox += '\t  @li ' + str(names) + '\n'
        
        dox += '\n\n'
        dox += '\t@section sec' + str(sec1) + '_' + str(sec2) + '_2     ' + str(sec1) + '.' + str(sec2) + '.2 引用说明\n'        
        for names in includes:
            dox += '\t  @li ' + str(names) + '\n'
            
        dox += '\n\n'
        dox += '\t@section sec' + str(sec1) + '_' + str(sec2) + '_3     ' + str(sec1) + '.' + str(sec2) + '.3 关键变量和内部结构定义\n'        
       
        dox += '''\t   无

\t@author xfhu
*/
        '''
        return dox
        
    
    def getdoxfunc(self, func, paras, rets):
        dox = '/** @brief  '+str(func)+'\n\n'
        
        dox += '\t     @par 函数功能: '+'\n\n'
        dox += '\t@param\n'
        for names in paras:
            dox += '\t  '+str(names)+'\n'
            
        dox+='\n\n'
        dox+='\t@return : ' +str(rets)+ '\n'
        if str(rets).find('int')>=0 :
            dox +=  '\t  @ret 0  成功\n\t  @ret -1  失败\n\n'
        elif str(rets).find('void')>=0 :
            dox += '\t @ret 无\n\n'
        else :
            dox += '\t  @ret \n\n'
            
        dox +='''
      @par 算法描述: 
        @li 无

      @par 关键变量及内部结构定义:
        @li 无

      @par 函数处理流程:
        @li 无        

      @par 数据库表使用：
        @li 无

      @par文件使用：
        @li 无

      @par IPC使用：
        @li 无

      @exception
        @li 参数检查失败

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
