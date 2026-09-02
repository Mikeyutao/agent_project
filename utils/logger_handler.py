#管理日志
import os
import logging
from datetime import datetime
from utils.path_tool import get_abs_path

#保存日志的根目录
LOG_ROOT = get_abs_path("logs") 

#确保日志目录存在
os.makedirs(LOG_ROOT, exist_ok=True)

DEFAULT_LOG_FORMAT = logging.Formatter(
    fmt="%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s"
    ) 

def get_logger(
        name:str = "agent",
        console_level:int = logging.INFO,
        file_level :int = logging.DEBUG,
        log_file = None)->logging.Logger:
    """
    创建日志对象
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG) 

    #避免重复添加处理器
    if logger.handlers:
        return logger

    #控制台Handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(console_level)     #指定日志级别，低于此级别的日志将不会被处理
    console_handler.setFormatter(DEFAULT_LOG_FORMAT)

    logger.addHandler(console_handler)

    #文件Handler
    if not log_file: 
        log_file = os.path.join(LOG_ROOT, f"{name}_ {datetime.now().strftime('%Y%m%d')}.log")

    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setLevel(file_level)
    file_handler.setFormatter(DEFAULT_LOG_FORMAT)

    logger.addHandler(file_handler)

    return logger

#快捷获取日志
logger = get_logger()

if __name__ == "__main__":
    logger.info("hello world")
    logger.error("error")
    logger.debug("debug")
    logger.warning("warning")
