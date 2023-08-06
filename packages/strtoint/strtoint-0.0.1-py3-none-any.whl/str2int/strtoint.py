import pinyin


def pinyin_2_hanzi(pinyinList, path_num):
    from Pinyin2Hanzi import DefaultDagParams
    from Pinyin2Hanzi import dag

    dagParams = DefaultDagParams()
    # path_num：候选值，可设置一个或多个
    result = dag(dagParams, pinyinList, path_num=path_num, log=True)
    re = []
    for item in result:
        # socre = item.score # 得分
        res = item.path  # 转换结果
        re.append(item.path)
    return re


class Strtoint():
    def __init__(self):
        self.____dic_str = 'abcdefghijklmnopqrstuvwxyz '
        self.____dic_str = self.____dic_str + self.____dic_str.upper()
        self.__dic = {}
        self.__dic1 = {}
        for y in range(len(self.____dic_str)):
            self.__dic[self.____dic_str[y]] = y
        for y in range(len(self.____dic_str)):
            self.__dic1[y] = self.____dic_str[y]

    def toint(self, text):
        try:
            int(text)
            raise OSError('the text parameter is not a int object')
            return None
        except:
            if text not in self.____dic_str:
                self.__text = pinyin.get(text, format='strip')
            else:
                self.__text = text
            rsp = ''
            for x in self.__text:
                rsp = rsp + '|' + str(self.__dic[x])
            return rsp[1:]

    def tostr(self, text, path_num=10):
        # if text not in self.____dic_str:
        #     self.__text = pinyin.get(text)
        # else:
        #     self.__text = text
        rsp = ''
        for x in str(text).split('|'):
            rsp = rsp + self.__dic1[int(x)]
        return rsp, {'候选项：': pinyin_2_hanzi([rsp], path_num)}
