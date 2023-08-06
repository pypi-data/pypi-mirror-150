# coding=utf-8
import hashlib
import random
import re
import string
import time
import os
import configparser
from oyeahz_base.logger.xlogger import logger


# 判断手机号是否有效
def is_phone_number_valid(phone_num: str) -> bool:
    if phone_num is None:
        return False
    if len(str(phone_num)) != 11:
        flag = False
    else:
        if not str(phone_num).isdigit():
            flag = False
        else:
            phone_rule = re.compile('^0\d{2,3}\d{7,8}$|^1[358]\d{9}$|^147\d{8}')
            res_list = re.findall(phone_rule, str(phone_num))
            if res_list:
                flag = True
            else:
                flag = False
    if flag:
        return True
    else:
        return False


# 判断邮箱是否有效
def is_email_valid(email: str) -> bool:
    if email is None:
        return False
    if re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", email) is not None:
        return True
    else:
        return False


# 获取任意长度的随机码
def get_random_code(length : int) -> str:
    source = '123456789'
    code = ''
    for i in range(length):
        num = random.randint(0, len(source) - 1)
        code += source[num]
    return code


# 创建一个随机长度的session
def gen_random_session(length: int) -> str:
    return ''.join(random.sample(string.ascii_letters + string.digits, length))


# 获取字符串MD5
def get_md5(input: str):
    return hashlib.md5(input.encode(encoding='UTF-8')).hexdigest()


# 当前时间，格式：年-月-日 时:分:秒
def get_current_time() -> str:
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


# 当前时间戳 毫秒级
def get_local_time_millis() -> int:
    return int(time.time() * 1000)


# 根据时间戳获取当前时间，格式：年-月-日 时:分:秒
def get_time(time_millis: int) -> str:
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time_millis / 1000))


# 根据时间字符串转为时间戳 秒级
def get_timestamp(time_str: str) -> int:
    return int(time.mktime(time.strptime(time_str, '%Y-%m-%d %H:%M:%S')))


# 根据时间戳获取当前日期，格式：年-月-日
def get_date(time_millis: int) -> str:
    return time.strftime("%Y-%m-%d", time.localtime(time_millis / 1000))


# 从字典获取值，不存在的key返回None
def dict_safe_get(input_dict: {}, key: str):
    param = None
    try:
        param = input_dict[key]
    except Exception as obj:
        logger.error(obj)
    return param


# 从数组获取值，不存在的index返回None
def array_safe_get(input_array: [], index: int):
    param = None
    try:
        param = input_array[index]
    except Exception as obj:
        logger.error(obj)
    return param


# 判断字符串是否空
def string_is_empty(input_str: str) -> bool:
    if input_str is None or input_str == '':
        return True
    return False


# 定义文件配置读取的类，oyeahz的本地配置全用这个配置文件
class ReadConfig:

    def __init__(self, filepath=None):
        if filepath:
            config_path = filepath
        else:
            root_dir = os.path.abspath('.')
            config_path = os.path.join(root_dir, "config.ini")
        self.cf = configparser.ConfigParser()
        self.cf.read(config_path)

    def get_config(self, key: str, param: str):
        value = self.cf.get(key, param)
        return value


# 根据本地文件配置的key取param对应的内容
def get_local_config(key: str, param: str):
    read_config = ReadConfig()
    return read_config.get_config(key, param)

