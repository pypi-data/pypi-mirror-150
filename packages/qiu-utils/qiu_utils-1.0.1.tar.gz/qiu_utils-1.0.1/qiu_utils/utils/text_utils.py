import re


remove_letters ='[【|】]'
def remove_nouse_letters(text):
    '''
    删除一些无关的字符
    :param text:
    :return:
    '''
    clean_text = re.sub(remove_letters,"",text)
    return clean_text

punctuation = {
    '：':":",
    "，":",",
    '．':'.',
    "（":"(",
    "）":")",
}

def clean_html_whitesplace(text):
    text = text.replace("&nbsp;","")
    text = text.replace("&nbsp", "")
    text = text.replace(" ","")
    text = text.replace('\n',"")
    text = text.replace("\t","")
    text = text.replace(' ',"")
    text = text.replace(' ', "")
    text = text.replace("\u3000","")
    text = text.replace("\r", "")
    return text

def replace_punctuation(text):
    '''
    将中文标点符号替换成英文
    :param text:
    :return:
    '''
    for key,value in punctuation.items():
        text = text.replace(key,value)

    return text

def clean_punctuation(text):
    for key,value in punctuation.items():
        text = text.replace(key,"")

    return text



def clean_text(text):
    text = remove_nouse_letters(text)
    text = clean_html_whitesplace(text)
    text = replace_punctuation(text)
    return text



if __name__ == '__main__':
    text_str= '名   称:苏州俊傲兴招投标代理有限公司'
    print(remove_nouse_letters(text_str))

