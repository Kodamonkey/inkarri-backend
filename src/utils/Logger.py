import logging
import os
import traceback


class Logger:
    def __set_logger(self):
        log_directory = 'src/utils/log'
        log_filename = 'app.log'
        
        
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.DEBUG)
        
        log_path = os.path.join(log_directory, log_filename)
        file_handler = logging.FileHandler(log_path, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        
        formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s | "%Y-%m-%d %H:%M:%S"')
        file_handler.setFormatter(formatter)
        
        if (logger.hasHandlers()):
            logger.handlers.clear()
            
        