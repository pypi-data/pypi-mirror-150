#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   mysql_utls.py    
@Contact :   fengfeng.qiu@amh-group.com

@Modify Time      @Author    
------------      -------    
2022/4/15 11:19   qiufengfeng      
'''
import pymysql
import pandas as pd

class MysqlConnector():
    def __init__(self,connect_info,table_name):
        self.mysql_conn = pymysql.Connect(**connect_info)
        self.table_name = table_name



    def update(self,update_dict,condition_dict):
        """
            update_dict 跟新的字段列表
            condition_dict 帅选字段列表

            这里实现上面偷懒了，没有字段类型做区分，统一用字符串的方式插入
        """
        sql = 'update {table_name} set '.format(table_name = self.table_name)

        set_list = []
        for (key, value) in update_dict.items():
            set_str = "%s=\"%s\"" % (key, value)
            set_list.append(set_str)
        condition_list = []
        for (key, value) in condition_dict.items():
            condition_str = "%s=\"%s\"" % (key, value)
            condition_list.append(condition_str)
        sql = sql + " " + ",".join(set_list)
        if condition_list:
            sql = sql + " where " + " and ".join(condition_list)

        mycursor = self.mysql_conn.cursor()
        mycursor.execute(sql)
        self.mysql_conn.commit()

    def make_insert_str(table_name, table_columns, values_list):
        '''
        on duplicate update user_name =values(user_name);
        :param table_name:要插入的表名
        :param table_columns:要插入的表的字段名
        :param values_list:
        :return:
        '''
        format_str = "insert into {table_name} {insert_columns} values {insert_values}"

        insert_columns = "(" + ",".join(table_columns) + ")"
        values_list = [["\"" + str(i) + "\"" for i in j] for j in values_list]
        values_list = ["(" + ",".join(i) + ")" for i in values_list]
        insert_values = ",\n".join(values_list)

        return format_str.format(table_name=table_name, insert_columns=insert_columns, insert_values=insert_values)

    def insert(self,table_columns,values_list):
        """
            update_dict 跟新的字段列表
            condition_dict 帅选字段列表

            这里实现上面偷懒了，没有字段类型做区分，统一用字符串的方式插入
        """
        format_str = "insert into {table_name} {insert_columns} values {insert_values}"

        insert_columns = "(" + ",".join(table_columns) + ")"
        values_list = [["\"" + str(i) + "\"" for i in j] for j in values_list]
        values_list = ["(" + ",".join(i) + ")" for i in values_list]
        #insert_values = ",\n".join(values_list)

        mycursor = self.mysql_conn.cursor()
        for value in values_list:
            sql = format_str.format(table_name=self.table_name, insert_columns=insert_columns, insert_values=value)
            mycursor.execute(sql)
        self.mysql_conn.commit()


    def select(self,select_list,condition_dict):
        '''
        select_list 需要读取的字段
        condition_dict 筛选条件
        '''
        if select_list:
            select_str = ",".join(select_list)
        else:
            select_str = "*"
        sql = 'select {select_str} from {table_name}'.format(select_str=select_str,table_name=self.table_name)

        condition_list = []
        for (key, value) in condition_dict.items():
            if "$$not$$" in value:
                value = value.replace("$$not$$","")
                condition_str = "%s!=\"%s\"" % (key, value)
            else:
                condition_str = "%s=\"%s\"" % (key, value)
            condition_list.append(condition_str)
        if condition_list:
            sql = sql + " where " + " and ".join(condition_list)

        labeled_data = pd.read_sql(sql, self.mysql_conn)
        return labeled_data

