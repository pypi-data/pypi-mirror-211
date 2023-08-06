import time
from datetime import datetime


def get_now_datetime_str():
    """
    返回当天时间
    :return:
    """
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))


def get_now_date_str():
    """
    返回当天日期
    :return:
    """
    return time.strftime('%Y-%m-%d', time.localtime(time.time()))


def get_now_time_str():
    """
    返回当前时间
    :return:
    """
    return time.strftime('%H:%M:%S', time.localtime(time.time()))


def get_date(date_str):
    """
    根据字符串获取日期
    :param str:
    :return:
    """
    return datetime.strptime(date_str, "%Y-%m-%d").date()


def get_datetime(date_str):
    """
    根据字符串获取日期
    :param str:
    :return:
    """
    return datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")


def get_days_between(start_str, end_str):
    """
    计算2个字符串日期 间隔天数
    :param start_str:
    :param end_str:
    :return:
    """
    return (datetime.strptime(start_str, "%Y-%m-%d") - datetime.strptime(end_str, "%Y-%m-%d")).days


if __name__ == '__main__':
    a = get_days_between("2023-01-01", "2021-09-08")
    print(type(a))
