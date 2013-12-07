from os.path import join, abspath, dirname
import sys
import logging.handlers

sys.path.append(abspath(join(dirname(__file__), r'../')))

from log import cloudshare_base_logger
import util
import log
import time

def get_logger(name):
    new_name = '%s.%s' % ('test_infra_base', name)
    return log.get_logger(new_name)
    
############################
# PassiveObject
############################
class PassiveObject(object):
    def __init__(self):
        self.logger = get_logger(type(self).__name__)

############################
# BackendInfraTest
############################
import unit
class BackendInfraTest(unit.TestCase):
    """ Base class for all Backend infra unit tests """
    def setUp(self): 
        # enable instance recording so the test instance is clean after the test
        self.configure_logs()
        self.b_record_instance_attributes = True
        def instance_cleanup():
            # Deleting all the test instance references, do not try to access any of them after this point
            for name in getattr(self, '_st_recorded_instances', set([])):
                try: delattr(self, name)
                except Exception, e: print 'Got exception while deleting attribute %s: %s' % (name,e)
            object.__setattr__(self, 'b_record_instance_attributes', False)
            util.do_GC()
            
        self.addCleanup(instance_cleanup)
        
    def configure_logs(self):
        backend_logger = logging.getLogger(cloudshare_base_logger)
        backend_logger.setLevel(logging.DEBUG)
        
        ### log formatting ###
        log_formatter = logging.Formatter('%(asctime)s thread=%(CSthreadName)s level=%(levelname)s logger=%(name)s {HostName=%(HostName)s} message=*M*| %(message)s |*M* process=%(processName)s pid=%(process)d')
        handler = logging.handlers.MemoryHandler(capacity=1024 * 1024) # 1 MB
        handler.setLevel(logging.ERROR)
        handler.setFormatter(log_formatter)
        backend_logger.addHandler(handler)        
            
    def __setattr__(self, name , value):
        if getattr(self,'b_record_instance_attributes', False):
            if not hasattr(self, '_st_recorded_instances'):
                object.__setattr__(self, '_st_recorded_instances', set([]))
            self._st_recorded_instances.add(name)
        object.__setattr__(self, name, value)
        
    def wait_until_true(self,f_condition,max_tries=5,sleep_time=500):
        for _ in xrange(max_tries):
            try:
                f_condition()
                break
            except Exception:
                time.sleep(sleep_time / 1000.0)
        f_condition()
