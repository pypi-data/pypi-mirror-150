from loguru import logger
import logging

from time import strftime
import os


class PropogateHandler(logging.Handler):
    def emit(self, record):
        logging.getLogger(record.name).handle(record)



class MyLog():
    __instance = None  # 单例实现
    __call_flag = True  # 控制init调用，如果调用过就不再调用

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    # def __init__(self):
    def get_log(self):
        if self.__call_flag:  # 看是否调用过
            __curdate = strftime('%Y%m%d-%H%M%S')
            logger.remove(handler_id=None)  # 关闭console输出
            logger.add('log/' + __curdate + '.log', encoding='utf8', # 日志存放位置
                       retention='2 days',  # 清理
                       rotation='10 MB',  # 循环 达到指定大小后建立新的日志
                       format='{time:YYYY-MM-DD HH:mm:ss},{module}(line:{line}),{level}|{message}',  # 日志输出格式
                       compression='zip',  # 日志压缩格式
                       level='INFO',
                       )  # 日志级别
            logger.add(PropogateHandler())
            self.__call_flag = False  # 如果调用过就置为False
        return logger

log = MyLog().get_log()

if __name__ == '__main__':
    print(os.path.dirname(__file__))

