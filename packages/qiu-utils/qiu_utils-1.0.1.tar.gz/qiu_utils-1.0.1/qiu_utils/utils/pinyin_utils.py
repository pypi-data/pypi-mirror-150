import pypinyin



def pinyin(word,upper_first_char=False):
    '''
    汉字转拼音
    :param word: 待转换word
    :param upper_first_char: 拼音第一个字符是否大写
    :return:
    '''
    s = ''
    for i in pypinyin.lazy_pinyin(word, style=pypinyin.NORMAL):
        if upper_first_char:
            s += ''.join(i.capitalize())
        else:
            s += ''.join(i)
    return s




if __name__ == '__main__':
    test = "江苏建设工程招标网"
    print(pinyin(test,upper_first_char=True))
    print(pinyin(test))