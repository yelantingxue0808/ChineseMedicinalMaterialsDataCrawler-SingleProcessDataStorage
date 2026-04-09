"""
@Author  : 孔天宇
@Desc    :
"""

from core import service
from utils import utils

if __name__ == '__main__':
    service.execute_task()
    # print(utils.build_select_db(table_name='text3', where_expr='id')% 1)
    # print(utils.build_insert_db(table_name='medical_table', fields=('name', 'age')))

