"""
@Author  : 孔天宇
@Desc    :
"""

import aiohttp
import asyncio
from lxml import etree
from config import https_settings
from utils import logger, utils


async def send_url(url, session):
    """
    向url发送请求
    """
    async with session.get(url) as response:
        response_data = response.text(encoding='utf-8')
        # get_logger().debug(f'{url}数据请求成功')
        return await response_data


async def parse_data(url):
    """
    解析数据
    """
    async with aiohttp.ClientSession(headers=https_settings.HEADERS) as session:
        # 阻塞等待，降低请求频率
        await asyncio.sleep(0.5)
        response_data = await send_url(url, session)
        # 使用xpath进行数据提取
        tree = etree.HTML(response_data, parser=None)
        all_list = []
        trs = tree.xpath("//tbody/tr")
        for tr in trs:
            try:
                item = {}
                tds = tr.xpath('./td[position()<9]')
                if len(tds) < 8:
                    continue

                item["品名"] = tds[0].xpath('./a[@title]/text()')[0] if tds[0].xpath('./a[@title]/text()') else ''
                item["规格"] = tds[1].xpath('./a[@title]/text()')[0] if tds[1].xpath(
                    './a[@title]/text()') else ''
                item["市场"] = tds[2].xpath('./text()')[0] if tds[2].xpath('./text()') else ''
                item["价格"] = tds[3].xpath('./text()')[0] if tds[3].xpath('./text()') else ''
                item["趋势"] = tds[4].xpath('./text()')[0] if tds[4].xpath('./text()') else ''
                item["周涨跌"] = tds[5].xpath('./text()')[0] if tds[5].xpath('./text()') else ''
                item["月涨跌"] = tds[6].xpath('./text()')[0] if tds[6].xpath('./text()') else ''
                item["年涨跌"] = tds[7].xpath('./text()')[0] if tds[7].xpath('./text()') else ''
                all_list.append(item)
                logger.get_logger().debug(f'{item}数据提取完成---{url}')
            except Exception as e:
                logger.get_logger().info(f'数据解析失败：{e}')
                continue
        # print('数据提的内容为：', item)
        return all_list


def task_process(urls, queue):
    """
    每个进程执行的任务
    """
    done = asyncio.run(utils.batch_asyncio(urls))  # 返回的是一个列表，列表中有多个字典
    for item in done:
        # 将字典放入队列中,每条数据单独放进队列
        queue.put(item)
    logger.get_logger().info(f"进程完成，放入队列 {len(done)} 条数据")
