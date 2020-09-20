from str_ing import colorful_print

class Table:
    '''
        优雅地在控制台输出表格

        通过修改self.HEADER_COLOR, self.DIVIDE_COLOR, self.ITEM_COLOR改变颜色
        （默认分别为"yellow","cyan","white"）
        （若str_ing.colorful_print.USE_COLOR==1，则不显示颜色）

        通过修改self.SHOW_HEADER决定是否显示表头
        （默认为1（显示））
    '''
    def __init__(self,header):
        self.SHOW_HEADER=1

        self.HEADER_COLOR="yellow"
        self.DIVIDE_COLOR="cyan"
        self.ITEM_COLOR="white"

        self.header=header
        self.data=[]

    def new_line(self,line):
        '''
        新建一行表格
        '''
        if len(line)<=len(self.header):
            self.data.append([str(i) for i in line])
            if len(self.data[-1])<len(self.header):#补全不完整部分
                self.data[-1].extend(
                    ["" for i in range(len(self.header)-len(self.data[-1]))]
                )
        else:
            raise ValueError("Line overflowed.")
    
    def __setitem__(self,key,item):
        if type(key)==type(tuple()):
            self.data[key[0]][key[1]]=str(item)
        elif type(key)==type(int()):

            if len(item)<len(self.header):#补全不完整部分
                item.extend(
                    ["" for i in range(len(self.header)-len(item))]
                )

            self.data[key]=item
        else:
            raise TypeError("Unexpected key type.")
        
    def __getitem__(self,key):
        if type(key)==type(tuple()):
            return self.data[key[0]][key[1]]
        elif type(key)==type(int()):
            return self.data[key]
        else:
            raise TypeError("Unexpected key type.")
    
    def __str__(self):
        """
        输出为字符串
        """
        if self.SHOW_HEADER:
            _header=[self.header]
            _header.extend(self.data)#把表头连接起来
            data=_header
        else:
            data=self.data
        
        max_row_length=[]
        for i in list(zip(*data)):#获得各行最大长度
            max_row_length.append(max([len(j.encode("gbk")) for j in i]))
        
        out=[]
        for ln in range(len(data)):
            line=[]
            for i in range(len(max_row_length)):
                line.append(colorful_print.color_str("|",fg=self.DIVIDE_COLOR))

                item=data[ln][i]
                length=max_row_length[i]-len(item.encode('GBK'))+len(item)
                _item='{item:<{len}}\t'.format(item=item,len=length)
                if ln==0 and self.SHOW_HEADER:
                    _item=colorful_print.color_str(_item,fg=self.HEADER_COLOR,dm="bold")
                else:
                    _item=colorful_print.color_str(_item,fg=self.ITEM_COLOR)
                line.append(_item)
                #对齐输出
                #代码修改自https://www.cnblogs.com/nul1/p/11136495.html
                #感谢dalao
            line.append(colorful_print.color_str("|",fg=self.DIVIDE_COLOR))
            out.append("".join(line))

        return "\n".join(out)