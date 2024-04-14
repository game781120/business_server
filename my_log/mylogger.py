from logging import getLogger, StreamHandler
from os.path import dirname, join
import logging
import os

parent_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
log_path = join(parent_path, "log.log")
logger = getLogger('public_logger')
logger.setLevel(logging.INFO)

# 如果已经存在其他Handler，避免重复记录
if not logger.handlers:
    file_handler = logging.FileHandler(log_path, encoding='utf-8')
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)

    # 创建输出到屏幕的Handler
    console_handler = StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    logger.info(f'create logger 初始化 {log_path}')