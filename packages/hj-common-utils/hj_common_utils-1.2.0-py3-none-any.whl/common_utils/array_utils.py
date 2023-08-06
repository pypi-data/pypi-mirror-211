def group_by(list_datas, field):
    """
    列表分组
    :param list_datas:分组列表
    :param field: 被分组字段名
    :return: 分组后的字典
    """
    # 创建一个空字典，用于存放分类后的结果
    classified_dict = {}
    # 遍历列表中的对象
    for list_data in list_datas:
        # 获取对象的age属性值
        field_data = list_data[field]
        # 检查分类字典中是否已经存在该年龄的键
        if field_data in classified_dict:
            # 如果存在，则将当前对象添加到对应的列表中
            classified_dict[field_data].append(list_data)
        else:
            # 如果不存在，则创建一个新的列表，并将当前对象添加到其中
            classified_dict[field_data] = [list_data]
    return classified_dict


def is_member(list_datas, data):
    """
    判断元素是否在列表中
    :param list_datas:
    :param data:
    :return:
    """
    return data in list_datas


def is_empty(list_datas):
    """
    判断列表是否为空
    :param list_datas:
    :return:
    """
    return len(list_datas) == 0
