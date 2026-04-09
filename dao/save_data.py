"""
@Author  : 孔天宇
@Desc    :
"""

from utils import logger, utils
from dao import database


def save_data(queue):
    """
    # 保存数据,单独一个进程，使用队列来接收解析+清洗后的数据
    """
    # 连接数据库
    db = database.Database().get_conn()
    # 设置字符
    db.set_charset(charset='utf8')
    # 创建游标对象
    cursor = db.cursor()
    count = 0

    try:
        logger.get_logger().info("开始保存数据到MySQL...")
        sql = utils.build_select_db(table_name='medical_table', where_expr='id')
        if cursor.execute(sql % 1):
            cursor.execute('truncate medical_table')
            # 循环读取队列所有数据
            while not queue.empty():
                # 每次都拿新数据
                # 在空队列时默认阻塞，一直等数据进来
                items = queue.get()
                # 不需要手动插入id,自动化管理
                sql = utils.build_insert_db(table_name='medical_table',
                                            fields=('品名', '规格', '市场', '价格', '趋势', '周涨跌', '月涨跌', '年涨跌'))
                cursor.execute(sql,
                               (items['品名'], items["规格"], items["市场"], items["价格"],
                                items["趋势"],
                                items["周涨跌"], items["月涨跌"],
                                items["年涨跌"]))
                count += 1
                # 提交事务
                db.commit()
        logger.get_logger().info(f'共保存{count}条数据')
    except Exception as error:
        print('数据库连接发生错误：', error)
        # 回滚事务
        db.rollback()

    # 关闭数据库
    cursor.close()
    db.close()
