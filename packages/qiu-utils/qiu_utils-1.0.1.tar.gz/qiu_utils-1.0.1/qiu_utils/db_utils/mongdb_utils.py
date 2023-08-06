import sys
from pymongo import MongoClient

if not sys.platform.startswith('win'):
    default_mongo_url = "mongodb://znlhadmin:Znlh1234@mongo:27017/mydb"
else:
    default_mongo_url = "mongodb://localhost:27017"


def get_mongo_connect(mongo_url = None,schema='construction'):
    connect_string  = mongo_url
    if connect_string != None:
        connect_string = default_mongo_url


    client = MongoClient(connect_string)
    return client,client[schema]

def update_item_status(search_dict,update_dict,mongo_table):
    '''
    跟新mongo db的数据
    :param search_dict: 查找的字段dict
    :param update_dict: 需要跟新的字段dict
    :param mongo_table: mongo table实例
    :return:
    '''
    new_values = {"$set":update_dict}
    mongo_table.update_one(search_dict,new_values)


def get_items(search_dict,mongo_table):
    '''
    :param search_dict: 查找的字段dict
    :param mongo_table: mongo tabel实例
    :return: 找到的数据item list
    '''
    items = mongo_table.find(search_dict)
    return items








