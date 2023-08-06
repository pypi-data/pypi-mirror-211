import os


def create_directory(directory_path):
    """
    判断文件夹是否存在 不存在创建
    :param directory_path:
    :return:
    """
    if not os.path.exists(directory_path):
        # 创建文件夹
        os.makedirs(directory_path)
        print(f"文件夹 '{directory_path}' 创建成功")
    else:
        print(f"文件夹 '{directory_path}' 已存在")


def is_dir(path):
    """
    是否是文件夹
    :param path:
    :return:
    """
    return os.path.isdir(path)
