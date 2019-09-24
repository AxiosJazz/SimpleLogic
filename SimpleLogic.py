# -*- coding:utf-8 -*-

sInput = ''     # 输入的命题公式字符串
sParse = ''     # 化简后的sInput
variable = []   # 保存公式中的变量
ornl = []       # 主析取范式最小项
andnl = []      # 主合取范式最大项
fore = ''       # 符号前面的部分
back = ''       # 符号后面的部分

def myinput():
    global sInput
    print("请输入一个任意命题公式(原子命题用字母表示,'~'表示非 '&'表示合取 '|'表示析取 '>'表示蕴含 ':'表示等价 '@'表示异或,可用括号'()'):")
    sInput = input()

def getVariale():
    global sInput, variable
    for c in sInput:
        if c >= 'A' and c <= 'Z' or c >= 'a' and c <= 'z' :
            if c not in variable:
                variable.append(c)
        elif c!='~' and c!='&' and c!='|' and c!='(' and c!=')' and c!='>' and c!=':' and c!='@':
            print('输入有误！！')
    variable = sorted(variable)

def getFB(c):
    global sInput, sParse, fore, back
    slen = len(sParse)
    for i in range(0,slen):             #遍历sParse中所有字符
        if sParse[i] is c:
            if sParse[i-1] is not ')':  #找到fore
                fore = sParse[i-1]
            else:
                flag = 1
                j = i - 2
                while flag is not 0:
                    if sParse[j] is '~':
                        j -= 1
                    if sParse[j] is '(':
                        flag -= 1
                    if sParse[j] is ')':
                        flag += 1
                    j -= 1
                fore = sParse[j+1 : i]
            if sParse[i+1] is not '(':  #找到back
                back = sParse[i+1]
            else:
                flag = 1
                j = i + 2
                while flag is not 0:
                    if sParse[j] is '~':
                        j += 1
                    if sParse[j] is ')':
                        flag -= 1         # flag表示括号层数
                    if sParse[j] is '(':
                        flag += 1
                    j += 1
                back = sParse[i+1 : j]
            if c is '>':
                sParse = sParse.replace(fore+'>'+back,'('+'~'+fore+'|'+back+')')
            elif c is ':':
                sParse = sParse.replace(fore+':'+back,'('+fore+'&'+back+')|(~'+fore+'&~'+back+')')
            elif c is '@':
                sParse = sParse.replace(fore+'@'+back,'~('+'('+fore+'&'+back+')|(~'+fore+'&~'+back+')'+')')

def parseInput():           # 转化命题公式中的>,:,@
    global sInput, sParse
    sParse = sInput
    getFB('>')
    getFB(':')
    getFB('@')

def cal():
    global sInput, sParse, variable, ornl, andnl, orResult, andResult
    vlen = len(variable)    # 变量个数
    n = 2**vlen             # 所有情况个数
    print('真值表如下：')
    print(variable, sInput+'即', sParse)
    for nl in range(0, n):  # 获取真值表
        value = []          # 数值
        j = nl              # 真值表当前行
        for i in range(0, vlen):
            value.append(0)
        i = 0
        while j != 0:
            value[i] = j % 2
            j = j // 2
            i += 1
        value.reverse()     # 反向列表中的元素
        value = list(map(str, value)) # 数字转字符
        s = sParse
        for x in range(0, vlen): # 使用具体真值替代变元
            s = s.replace(variable[x], value[x])
        result = eval(s) & 1 # 利用eval函数直接求解
        if result is 1:
            ornl.append(nl)
        else:
            andnl.append(nl)
        print(value, result)

def outprint():
    print('主析取范式：')
    print('∑', ornl, sep='')
    print('主合取范式：')
    print('∏', andnl, sep='')

def main():
    myinput()
    getVariale()
    parseInput()
    cal()
    outprint()

if __name__=='__main__':
    main()