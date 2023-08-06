# coding=utf-8
import pymysql
import re
from pymysql.connections import Connection
from oyeahz_base.logger.xlogger import logger
from oyeahz_base.utils import oyeahz_utils


# 获取mysql数据库实例
def get_database(host: str, user: str, password: str, database: str) -> Connection:
    db = None
    try:
        db = pymysql.connect(host=host, user=user, password=password, database=database, charset='utf8')
    except Exception as obj:
        logger.error(obj)
    return db


# 通过本地配置获取mysql数据库实例
def get_database_by_local_key(key: str, database: str) -> Connection:
    db = None
    try:
        host = oyeahz_utils.get_local_config(key, 'host')
        user = oyeahz_utils.get_local_config(key, 'user')
        password = oyeahz_utils.get_local_config(key, 'password')
        db = get_database(host, user, password, database)
    except Exception as obj:
        logger.error(obj)
    return db


# 判断数据库中表是否存在
def table_exists(database: Connection, table_name: str) -> bool:
    if database is None:
        return False
    try:
        cursor = database.cursor()
        show_table_sql = "show tables;"
        cursor.execute(show_table_sql)
        tables = [cursor.fetchall()]
        table_list = re.findall('(\'.*?\')', str(tables))
        table_list = [re.sub("'", '', each) for each in table_list]
        if table_name in table_list:
            return True
        else:
            return False
    except Exception as obj:
        logger.error(obj)


def where_and_condition(where_info: dict) -> str:
    sql = ""
    where_condition_list = where_info.keys()
    if len(where_condition_list) > 0:
        sql = " WHERE"
        for column in where_condition_list:
            value = where_info[column]
            if type(value) is int or type(value) is float:
                sql += " " + column + "=" + str(value) + ""
            else:
                sql += " " + column + "=\'" + where_info[column] + "\'"
            sql += " AND"
        sql = sql[:-4]
    return sql


def where_or_condition(where_info: dict) -> str:
    sql = ""
    where_condition_list = where_info.keys()
    if len(where_condition_list) > 0:
        sql = " WHERE"
        for column in where_condition_list:
            value = where_info[column]
            if type(value) is int or type(value) is float:
                sql += " " + column + "=" + str(value) + ""
            else:
                sql += " " + column + "=\'" + where_info[column] + "\'"
            sql += " OR"
        sql = sql[:-4]
    return sql


def or_condition(where_info: dict) -> str:
    sql = ""
    where_condition_list = where_info.keys()
    if len(where_condition_list) > 0:
        sql = ""
        for column in where_condition_list:
            value = where_info[column]
            if type(value) is int or type(value) is float:
                sql += column + "=" + str(value) + ""
            else:
                sql += column + "=\'" + where_info[column] + "\'"
            sql += " OR "
        sql = sql[:-4]
    return sql


def and_condition(where_info: dict) -> str:
    sql = ""
    where_condition_list = where_info.keys()
    if len(where_condition_list) > 0:
        sql = ""
        for column in where_condition_list:
            value = where_info[column]
            if type(value) is int or type(value) is float:
                sql += column + "=" + str(value) + ""
            else:
                sql += column + "=\'" + where_info[column] + "\'"
            sql += " AND "
        sql = sql[:-5]
    return sql


def gen_insert_sql(table_name: str, column_info: dict) -> str:
    column_list = column_info.keys()
    sql = 'INSERT INTO %s (' % table_name
    for column in column_list:
        sql += "'" + column + "',"
    sql = sql[:-1]
    sql += ") VALUES ("
    for column in column_list:
        value = column_info[column]
        if type(value) is int or type(value) is float:
            sql += str(value) + ","
        else:
            sql += "\'" + value + "\',"
    sql = sql[:-1] + ");"
    return sql


def gen_update_sql(table_name: str, update_info: dict, where_info: dict) -> str:
    column_list = update_info.keys()
    sql = "UPDATE %s SET " % table_name
    for column in column_list:
        value = update_info[column]
        if type(value) is int or type(value) is float:
            sql += column + "=" + str(update_info[column]) + ","
        else:
            sql += column + "=\'" + str(update_info[column]) + "\',"
    sql = sql[:-1]
    sql += where_and_condition(where_info)
    sql += ";"
    return sql


# 生成查询sql
def gen_single_select_sql(table_name: str, column_list: list, where_info: dict) -> str:
    sql = "SELECT "
    if len(column_list) > 0:
        sql += ','.join(str(column) for column in column_list)
    else:
        sql += "*"
    sql += " FROM %s " % table_name
    sql += where_and_condition(where_info)
    sql += ";"
    return sql


def gen_delete_sql(table_name, where_info: dict) -> str:
    sql = "DELETE %s " % table_name
    sql += where_and_condition(where_info)
    sql += ";"
    return sql
