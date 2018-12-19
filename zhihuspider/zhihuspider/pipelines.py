# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from .items import *
from twisted.enterprise import adbapi
import pymysql

class ZhihuspiderPipeline(object):
    def __init__(self):
        # 链接数据库，创建游标
        pass

    def process_item(self, item, spider):
        if isinstance(item, ZhihuAnswerItem):
            # 设置sql语句
            # 调用execute()
            # 提交commit()至答案表
            pass
        elif isinstance(item, ZhihuQuestionItem):
            # 设置sql语句
            # 调用execute()
            # 提交commit()至问题表
            pass
        return item


class ZhihuMysqlPipeline(object):
    def __init__(self, pool):
        self.dbpool = pool

    @classmethod
    def from_settings(cls, settings):
        """
        这个函数名称是固定的，当爬虫启动的时候，scrapy会自动调用这些函数，加载配置数据。
        :param settings:
        :return:
        """
        params = dict(
            host=settings['MYSQL_HOST'],
            port=settings['MYSQL_PORT'],
            db=settings['MYSQL_DB'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWD'],
            charset=settings['MYSQL_CHARSET'],
            cursorclass=pymysql.cursors.DictCursor
        )

        # 创建一个数据库连接池对象，这个连接池中可以包含多个connect链接对象。
        # 参数1：操作数据库的包名
        # 参数2：链接数据库的参数
        db_connect_pool = adbapi.ConnectionPool('pymysql', **params)

        # 初始化这个类的对象
        obj = cls(db_connect_pool)
        return obj

    def process_item(self, item, spider):
        """
        在连接池中，开始执行数据的多线程写入操作。
        :param item:
        :param spider:
        :return:
        """
        # 参数1：在线程中被执行的sql语句
        # 参数2：要保存的数据
        result = self.dbpool.runInteraction(self.insert, item)
        # 给result绑定一个回调函数，用于监听错误信息
        result.addErrback(self.error)
        # result.addCallback()

    def error(self, reason):
        print('--------', reason)

    def insert(self, cursor, item):
        if isinstance(item, ZhihuAnswerItem):
            # 设置sql语句
            # 调用execute()
            # 提交commit()至答案表

            # 长度255指的是所保存数据的最大字符长度(内存所占字节)。
            # varchar: 255  '123'(开辟3个字节的空间)
            # char: 255  '123'(开辟255个字节的空间)
            # longtext
            # text
            insert_sql = 'INSERT INTO answer(answer_id, answer_question_id, answer_vote_up_nums) VALUES (%s, %s, %s)'
            cursor.execute(insert_sql, (item['answer_id'], item['answer_question_id'], item['answer_vote_up_nums']))
        elif isinstance(item, ZhihuQuestionItem):
            # 设置sql语句
            # 调用execute()
            # 提交commit()至问题表

            insert_sql = 'INSERT INTO question(question_id, question_title) VALUES (%s, %s)'
            cursor.execute(insert_sql, (item['question_id'], item['question_title']))


