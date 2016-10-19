import logging

class janus_logger(object):
    
    __prefix = "JANUS: "
    __enabled = True
    
    @classmethod
    def enable(cls):
        cls.enabled = True
    
    @classmethod 
    def disable(cls):
        cls.enabled = False
    
    @classmethod
    def debug(cls, message):
        if cls.enabled: logging.debug(cls.__prefix + message)
        
    @classmethod
    def info(cls, message):
        if cls.enabled: logging.info(cls.__prefix + message)
        
    @classmethod
    def warning(cls, message):
        if cls.enabled: logging.warning(cls.__prefix + message)
        
    @classmethod
    def error(cls, message):
        if cls.enabled: logging.error(cls.__prefix + message)
        
    @classmethod
    def critical(cls, message):
        if cls.enabled: logging.critical(cls.__prefix + message)