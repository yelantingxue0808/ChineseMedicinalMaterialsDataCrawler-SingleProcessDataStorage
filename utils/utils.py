"""
@Author  : 孔天宇
@Desc    :
"""

from config.settings import PageConfig
from config import settings
from core import handler
import asyncio


def get_url():
    """
    获取所有的url
    """
    urls = [settings.URL.format(page) for page in range(PageConfig.START + 1, PageConfig.STOP + 1)]
    return urls


def split_url():
    """
    将122页的url分成4片
    """
    urls_ = get_url()
    url_list = [urls_[index:index + PageConfig.STEP] for index in
                range(PageConfig.START, PageConfig.STOP, PageConfig.STEP)]
    return url_list


async def batch_asyncio(urls):
    """
    协程批量执行任务
    """
    tasks = []
    for url in urls:
        coroutine = handler.parse_data(url)
        task = asyncio.create_task(coroutine)
        tasks.append(task)
    data_list = await asyncio.gather(*tasks)
    item_list = []
    for data in data_list:
        item_list.extend(data)
    return item_list


def build_select_db(table_name, fields=None, where_expr=None, logic=None):
    """
    select *from table where id=1 and name=a
    logic={'and': "name"}
    :return:
    """
    fields = fields or []
    fields = ','.join(fields) or '*'
    sql = f'select {fields} from {table_name}'
    if where_expr:
        sql += f' where {where_expr}=%s'
        logic = logic or {}
        for key, val in logic.items():
            sql += f' {key} {val}=%s '
    return sql


def build_insert_db(table_name, fields=None):
    fields = fields or []
    val_exr = ['%s'] * len(fields)
    fields = ','.join(fields) or ''
    val_exr = ','.join(val_exr)
    sql = f'insert into {table_name}({fields}) values({val_exr})'
    return sql
