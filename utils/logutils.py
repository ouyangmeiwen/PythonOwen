import logging

class LogUtils:
    @staticmethod
    def setup_logger(log_file='app.log', level=logging.INFO, console_output=True):
        """
        设置日志配置
        :param log_file: 日志文件名
        :param level: 日志等级
        :param console_output: 是否同时输出到控制台
        """
        logger = logging.getLogger()
        if not logger.hasHandlers():  # 防止重复添加 Handler
            logger.setLevel(level)
            formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

            # 文件日志
            file_handler = logging.FileHandler(log_file)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)

            # 控制台日志
            if console_output:
                console_handler = logging.StreamHandler()
                console_handler.setFormatter(formatter)
                logger.addHandler(console_handler)
        return logger

    @staticmethod
    def log_debug(message):
        """记录调试日志"""
        logger = logging.getLogger()
        logger.debug(message)

    @staticmethod
    def log_info(message):
        """记录信息日志"""
        logger = logging.getLogger()
        logger.info(message)

    @staticmethod
    def log_warning(message):
        """记录警告日志"""
        logger = logging.getLogger()
        logger.warning(message)

    @staticmethod
    def log_error(message):
        """记录错误日志"""
        logger = logging.getLogger()
        logger.error(message)

    @staticmethod
    def log_critical(message):
        """记录严重错误日志"""
        logger = logging.getLogger()
        logger.critical(message)

    @staticmethod
    def change_log_level(level):
        """动态修改日志等级"""
        logger = logging.getLogger()
        logger.setLevel(level)

        
if __name__ == "__main__":
    # 设置日志配置
    logger = LogUtils.setup_logger(log_file='application.log', level=logging.DEBUG, console_output=True)
    
    # 调试日志
    LogUtils.log_debug("This is a debug message.")
    
    # 信息日志
    LogUtils.log_info("Application started successfully.")
    
    # 警告日志
    LogUtils.log_warning("This is a warning message.")
    
    # 错误日志
    LogUtils.log_error("An error occurred while processing data.")
    
    # 严重错误日志
    LogUtils.log_critical("Critical system failure detected.")
    
    # 动态修改日志等级为 WARNING
    LogUtils.change_log_level(logging.WARNING)
    
    # 此时，低于 WARNING 等级的日志不会输出
    LogUtils.log_info("This info log will not be shown.")
    LogUtils.log_warning("This warning log will be shown.")
