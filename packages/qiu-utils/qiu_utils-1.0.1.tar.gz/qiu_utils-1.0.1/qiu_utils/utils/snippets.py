
def combine_two_dict(dict_a,dict_b):
    '''
    合并两个dict
    :param dict_a:
    :param dict_b:
    :return:
    '''
    for key,value in dict_a.items():
        if key in dict_b:
            if type(dict_a[key]) == dict and type(dict_b[key]) == dict:
                dict_a[key] = combine_two_dict(dict_a[key],dict_b[key])
            elif type(dict_a[key]) == list:
                if type(dict_b[key]) == list and len(dict_b[key]) and type(dict_b[key][0]) == 'dict':
                    dict_a[key] = combine_list_to_list(dict_a[key],dict_b[key])
                else:
                    for item in dict_b[key]:
                        if item not in dict_a[key]:
                            dict_a[key].append(item)                   
            else:
                dict_a[key] = dict_b[key]

    for key,value in dict_b.items():
        if key not in dict_a:
            dict_a[key] = dict_b[key]
    return dict_a

def convert_valuelist_to_str(info_dict,list_keys):
    for key,value in info_dict.items():
        if type(value) == dict:
            convert_valuelist_to_str(info_dict[key],list_keys)
        else:
            if type(value) == list and key not in list_keys:
                info_dict[key] = "".join(value)



def replace_dict_value(dict_to_replace,old_value,new_value):
    '''
    将字典中的指定old_value替换为new_value
    :param dict_to_replace:
    :param old_value:
    :param new_value:
    :return:
    '''
    for key,value in dict_to_replace.items():
        if type(dict_to_replace[key]) == dict:
            replace_dict_value(dict_to_replace[key],old_value,new_value)
        else:
            if type(dict_to_replace[key]) == list:
                if old_value in dict_to_replace[key]:
                    new_list = [x if x != old_value else new_value for x in dict_to_replace[key] ]
                    dict_to_replace[key] = new_list
            else:
                if dict_to_replace[key] == old_value:
                    dict_to_replace[key] = new_value


def combine_list_to_list(list_a,list_b):
    '''
    蒋两个list,元素为dict的列表进行合并
    :param list_a:
    :param list_b:
    :return:
    '''
    for item in list_b:
        list_a = combine_dict_to_list(list_a,item)
    return list_a



def combine_dict_to_list(list_a,dict_b):
    '''
    蒋一个dict_b内容合并到一个lista里面去
    :param list_a:
    :param dict_b:
    :return:
    '''
    check_b_key = ""
    for key in dict_b.keys():
        if '名称' in key:
            check_b_key = key
            break
    has_combine = False
    for item in list_a:
        check_a_key = ""
        for key in item.keys():
            if '名称' in key:
                check_a_key = key
                break


        if check_a_key and check_b_key:
            if item[check_a_key] == dict_b[check_b_key]:
                combine_two_dict(item,dict_b)
                has_combine = True
                break
    if not has_combine:
        list_a.append(dict_b)
    return list_a

