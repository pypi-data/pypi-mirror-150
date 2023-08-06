from triedTree.base_tried_tree import BaseTriedTree
import os


class InfoTriedTree(BaseTriedTree):
    def __init__(self,path):
        super(InfoTriedTree,self).__init__(path=path)

    def _load_data_tree(self,file_or_path,type_prefix=None):
        total_file = []
        if not os.path.isfile(file_or_path):
            files = os.listdir(file_or_path)
            for file in files:
                real_path = os.path.join(file_or_path, file)
                if type_prefix == None:
                    new_type_prefix = file
                else:
                    new_type_prefix = type_prefix + "_" + file
                if os.path.isdir(real_path):
                    self._load_data_tree(real_path,type_prefix=new_type_prefix)
                else:
                    total_file.append((real_path,new_type_prefix))
        else:
            total_file.append((file_or_path,type_prefix))

        for file_and_type in total_file:
            self._add_file_to_tree(file_and_type)

    def _add_file_to_tree(self,file_and_type):
        '''从文件中读取数据'''
        filename,type_prefix = file_and_type
        with open(filename,'r',encoding='utf-8') as fread:
            for line in fread:
                line  = line.strip()
                if line == "":
                    continue
                token_list = line.split(" ")
                word = token_list[0]
                self._insert_word_and_type_to_tree(word,type_prefix)

    def process(self,content):
        cn_chars = content
        word_list = []
        type_list = []
        position_list = []
        tmp_search_word = []

        current_position = 0
        while len(cn_chars) > 0:
            word_tree = self.trie_tree
            current_word = ""  # 当前词
            for (index, cn_char) in enumerate(cn_chars):
                if cn_char not in word_tree:
                    break
                current_word += cn_char
                # 词结束
                if 'end' in word_tree[cn_char]:
                    tmp_search_word.append((current_word,index, word_tree[cn_char]['type_list']))
                word_tree = word_tree[cn_char]  # 继续深搜


            # 没有找到以这个字开头的词，继续下一个字
            if len(tmp_search_word) == 0:
                cn_chars = cn_chars[1:]
                current_position += 1
            else:

                word,index,type = tmp_search_word[-1]
                word_list.append(word)
                type_list.append(type)
                current_position += len(word)
                position_list.append(current_position)
                cn_chars = cn_chars[index +1:]
                tmp_search_word = []


        return word_list, type_list,position_list

    def get_word_types(self,word):
        types = []
        word_tree = self.trie_tree
        for (index, cn_char) in enumerate(word):
            if cn_char not in word_tree:
                break
            # 词结束
            if 'end' in word_tree[cn_char] and index == (len(word) - 1):
                types = word_tree[cn_char]['type_list']
            word_tree = word_tree[cn_char]  # 继续深搜

        return types


