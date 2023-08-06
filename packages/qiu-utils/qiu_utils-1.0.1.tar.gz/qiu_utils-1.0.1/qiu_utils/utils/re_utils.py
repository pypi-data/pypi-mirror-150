import re

def match_string(pattern,text):
    text = text.strip()
    match = re.findall(pattern,text)
    if match:
        return match
    else:
        return  []

def match_one(pattern,text):
    '''
    默认pattern里面只有一个()
    :param pattern:
    :param text:
    :return:
    '''
    text = text.strip()
    match = re.match(pattern,text)
    if match:
        return match[1]
    else:
        return ""


def search_one(pattern,text):
    '''
    默认pattern里面只有一个()
    :param pattern:
    :param text:
    :return:
    '''
    text = text.strip()
    match = re.search(pattern,text)
    if match:
        return match[1]
    else:
        return ""






if __name__ == '__main__':
    text = '项目名称：苏州市体育中心大维修工程（体育场增加屋顶消防水箱）   项目名称：ra'
    #pattenr = "项目名称：(\S*)"
    #print(match_string(pattenr,text))

