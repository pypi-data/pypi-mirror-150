import os

def get_files(fold):
    '''
    获取某个目录下面的所有文件
    '''
    result = []
    for file_or_folder  in os.listdir(fold):
        rel_path = os.path.join(fold,file_or_folder)
        if os.path.isdir(rel_path):
            result += get_files(rel_path)
        else:
            result.append(rel_path)
    return result



if __name__ == '__main__':
    pass
