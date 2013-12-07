import logging
import socket
import threading
hostname = socket.gethostname()

cloudshare_base_logger = 'cs'

class ExtraInfo(object):
    '''according to a recipe from:
    http://docs.python.org/howto/logging-cookbook.html#adding-contextual-information-to-your-logging-output'''
    def __getitem__(self, name):
        """To allow this instance to look like a dict."""
        if name == 'CSthreadName':
            return threading.current_thread().name
        if name == 'HostName':
            return hostname
        return self.__dict__.get(name, '?')
    
    def __iter__(self):
        """To allow iteration over keys, which will be merged into the LogRecord dict before formatting and output.
        """
        keys = ['CSthreadName', 'HostName']
        keys.extend(self.__dict__.keys())
        return keys.__iter__()

def get_logger(name, b_raw_name=False):
    """Returns application logger for given name. If name is null returns
       The main logger for the application.
    """
    if b_raw_name:
        logger = logging.getLogger(name)
    else:
        logger = logging.getLogger(cloudshare_base_logger + '.' + name)
    adapter = logging.LoggerAdapter(logger, ExtraInfo())
    # re-route log methods to adapter methods to handle the 'extra' context
    # supporting both lower case and upper case syntax
    adapter.Debug = adapter.debug
    adapter.Info = adapter.info
    adapter.Warn = adapter.warning
    adapter.Error = adapter.error
    adapter.Critical = adapter.critical
    adapter.name = adapter.logger.name
    adapter.addHandler = adapter.logger.addHandler
    adapter.removeHandler = adapter.logger.removeHandler 
    return adapter


class SimpleLogger(object):
    """Base class for implementing simple loggers.
       Derived classes only need to override the method 'log'
    """
    def __init__(self, name):
        self.name = name

    def Debug(self,msg): self.log('Debug',msg)
    def Info(self,msg): self.log('Info',msg)
    def Warn(self,msg): self.log('Warn',msg)
    def Error(self,msg): self.log('Error',msg)
    def Fatal(self,msg): self.log('Fatal',msg)

    def log(self, level, msg):
        raise Exception('NOT IMPLEMENTED')

class SimpleBufferLogger(SimpleLogger):
    def __init__(self): 
        self.name = 'SimpleBufferLogger'
        super(SimpleBufferLogger, self).__init__(self.name)
        self.buffer = []
    def reset(self): 
        self.buffer = []
    def log(self, level,msg): 
        self.buffer.append('%s: %s' % (level, msg))

def get_class_logger(obj):
    """Convenience method for getting a canonical logger name based on the type name of a given object"""
    return get_logger(name=type(obj).__name__)
