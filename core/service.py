"""
@Author  : 孔天宇
@Desc    :
"""

from multiprocessing import Process, Manager
from utils import utils, logger
from core import handler
from dao import save_data


def execute_task():
    queue = Manager().Queue()
    processes = []
    for urls in utils.split_url():  # 4个进程，每个进程解析35个url数据
        p = Process(target=handler.task_process, args=(urls, queue))
        p.start()
        processes.append(p)

    for pro in processes:
        pro.join()

    # 单独启动1个进程，执行数据保存（关键：爬取完成后再保存）
    save_process = Process(target=save_data.save_data, args=(queue,))
    save_process.start()
    save_process.join()
    logger.get_logger().info('全部爬取完成')
