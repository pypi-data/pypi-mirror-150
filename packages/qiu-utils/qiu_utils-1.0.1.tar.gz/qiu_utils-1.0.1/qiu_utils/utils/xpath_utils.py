

def get_alltext(node):
    '''
    获取一个节点下面的所有文本
    :param node:
    :return:
    '''
    texts_node = node.xpath(".//text()").extract()
    text_str = ""
    for text in texts_node:
        text_str += text
    return text_str

def get_first_trs(table_node,pattern = './*'):
    nodes = table_node.xpath(pattern)
    found_tr = False
    for node in nodes:
        if node.root.tag == 'tr':
            found_tr = True
            break

    if found_tr:
        pattern = pattern[:-2] + '/tr'
        nodes = table_node.xpath(pattern)
    else:
        nodes =  get_first_trs(table_node,pattern+'/*')
    return nodes


def get_all_tables(root_node):
    '''
    获取一个节点下面的所有的table节点
    :param root_node:
    :return:
    '''
    table_nodes = root_node.xpath(".//table")
    #if len(table_nodes):
    #    for table_node in table_nodes:
    #        sub_tables = get_all_tables(table_node)
    #        table_nodes.extend(sub_tables)

    return table_nodes