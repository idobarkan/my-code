import os

from enum import Enum
import log
MsgType = Enum('MsgType', ['Assertion','Warning']) #@ReservedAssignment

class AssertionException(AssertionError):
    Message = Exception.message 

def default_formatter(msg,kw):
    try:
        str_kw = ', '.join(('%s=%s' % (k,v)) for k,v in kw.iteritems())
        str_info = '%s. %s' % (msg, str_kw)
    except:
        str_info = 'ASSERTION. NO INFO - ERROR WHILE FORMATTING ARGS!'
    return str_info

def default_alert_sender(logger, msg_type, msg, **kw):
    str_info = default_formatter(msg,kw)
    
    if msg_type == MsgType.Assertion:
        logger.Error(str_info)
    else:
        logger.Warn(str_info)

class Assertions(object):
    def __init__(self):
        self.TEST_reset_config()
        self.reset_events()
        self.logger = log.get_class_logger(self)
    
    def TEST_reset_config(self):
        self.logger = log.get_logger('Assertions') # will propagate to root logger unless overidden
        self.alert_sender = default_alert_sender # can be overriden
        
        self._exit = os._exit # exit immediately, without cleanup
        self.b_fail_is_fatal = False # whether to throw exception or exit immediately on failure (for debugging)
        
    def reset_events(self):
        self.had_assertion = False

    def _end_program(self):
        self.logger.Fatal('ENDING PROGRAM DUE TO ASSERTION!')
        self._exit(-1) 

    def on_fail(self, msg, b_fatal):
        if b_fatal or self.b_fail_is_fatal:
            self.logger.Fatal(msg)
            self._end_program()
        raise AssertionException(msg)
        
    def _send_alert(self, msg_type, msg, kw, logger):
        if logger is None:
            logger = self.logger
        self.had_assertion = True
        formatted_msg = self.alert_sender(logger, msg_type, msg, **kw)
        return formatted_msg
    
Assertions = Assertions()

##################################################

def end_program():
    Assertions._end_program()

def fail(msg, logger=None, b_fatal=False, **kw):
    if callable(msg):
        msg = msg()
    formatted_msg = Assertions._send_alert(MsgType.Assertion,msg,kw,logger=logger) 
    if not formatted_msg:
        formatted_msg = default_formatter(msg,kw)
    Assertions.on_fail(formatted_msg, b_fatal=b_fatal)

def fail_if(cond,msg,logger=None, b_fatal=False, **kw):
    if cond:
        fail(msg, logger=logger, b_fatal=b_fatal, **kw)

def fail_unless(cond, msg, logger=None, b_fatal=False, **kw):
    if not cond:
        fail(msg, logger=logger, b_fatal=b_fatal, **kw)

def assert_that(cond, msg, logger=None, b_fatal=False, **kw):
    if not cond:
        fail(msg, logger=logger, b_fatal=b_fatal, **kw)

def warn(msg, logger=None, **kw):
    Assertions._send_alert(MsgType.Warning, msg, kw, logger=logger) 

def warn_if(cond,msg,logger=None, **kw):
    if cond:
        warn(msg, logger=logger, **kw)

def warn_unless(cond, msg, logger=None, **kw):
    if not cond:
        warn(msg, logger=logger, **kw)

