from util import synchronized, RLock, fmt_exc, DTO
import assertions
from functools import partial
import random
import threading
class FutureTimeoutException(Exception):
    pass

############################
# Progress Details (has C# Shadow)
############################
class ProgressDetails(DTO):
    _code_version = 0
    def __init__(self,
                 is_set,
                 percent, # int
                 error, # exception (can be None)
                 ):
        super(ProgressDetails,self).__init__(locals())

    @property
    def is_error(self): 
        return self.error is not None

############################
# FutureValue (has C# shadow)
############################
class FutureValue(DTO):
    _code_version = 0
    def __init__(self,
                 value, # can be none
                 progress, # ProgressDetails
                 ):
        super(FutureValue,self).__init__(locals())
        if False:
            self.progress = ProgressDetails()

def checkpoint(name):
    """Used to provide yield points in AO for hook manager""" 
    return Future.preset(None).set_name(name)

############################
# Future
############################
class Future(object):
    def __init__(self):
        self._event = None # create event on demand if someone calls wait()
        self._is_set = False
        self._lock = RLock() # used by @synchronized() decorator
        self._val = None
        self._exc = None
        self._progress_percent = 0 # XXX - need to handle 0 and 100 special cases if we want to use non-int progress types (e.g. with stages, or even float...)
        self._lst_observers = [] # list of (observer,b_notify_on_progress)
        self.name = None # can be set to help identify the future
        self.Id = random.getrandbits(63)
        self.caller_progress_increment = None
        self.caller_progress_to = None

    def __str__(self):
        progress = self.get_progress()
        if progress.is_set:
            if progress.is_error:
                str_body = "Error"
            else:
                str_body = '%s' % (self._val,)
        else:
            str_body = "%s%% ready" % (progress.percent,)
        
        s = "Future(Name:%s %s)" % (self.name, str_body,)
        if type(s) is unicode:
            return s.encode('raw_unicode_escape')
        else:
            return s
    
    def set_name(self,name):
        self.name = name
        return self

    @synchronized()
    def attach_observer(self,observer,b_notify_on_progress=False,b_notify_once=False,b_notify_immediate_progress=True):
        """observer(future) is called when future is set.
        observers attached after future is set will be called immediately (from same thread)"""
        b_notified = False
        if self.is_set() or (b_notify_on_progress and b_notify_immediate_progress and self._progress_percent > 0):
            observer(self)
            b_notified = True
        if not b_notify_once or not b_notified:
            self._lst_observers.append((observer, b_notify_on_progress, b_notify_once))

    @synchronized()
    def set_val_or_error(self,val=None,exc=None):
        if self.is_set():
            if isinstance(self._exc,FutureTimeoutException) or isinstance(exc, FutureTimeoutException):
                return # nothing to do. future was set with timeout already
            else:
                assertions.fail("Future is already set", exc=self._exc, new_exc=exc, val=self._val, f=self, new_val=val)
        if exc is not None: # check exc and not val. value can be legitimately set to None.
            self._exc = exc
            self._progress_percent = 0 # don't call set_progress (no need to trigger another update)
        else:
            self._val = val
            self._progress_percent = 100 # don't call set_progress (no need to trigger another update)
        self._is_set = True # must do this before _event.set(), so released threads can assert f.is_set()
        if self._event is not None:
            self._event.set()
        self._notify_observers(b_progress=False)

    def _notify_observers(self,b_progress, b_allow_regression = False):
        lst = self._lst_observers
        self._lst_observers = []
        for obs_info in lst:
            obs,b_notify_on_progress,b_notify_once = obs_info
            b_keep = True
            if b_notify_on_progress or not b_progress:
                if b_notify_once:
                    b_keep = False
                try:
                    obs(self, b_allow_regression = b_allow_regression)
                except Exception, e:
                    assertions.warn("Future got exception while calling observer.", observer=obs, exc=fmt_exc(e))
            if b_keep:
                self._lst_observers.append(obs_info)

    def set(self,val): #@ReservedAssignment
        self.set_val_or_error(val=val)
    def set_error(self,exc):
        self.set_val_or_error(exc=exc)

    def set_by_other_future_value(self,f):
        val,exc = f.get_val_or_error()
        self.set_val_or_error(val=val,exc=exc)
        
    @synchronized()
    def set_progress(self,percent,b_allow_regression=False):
        if self.is_set():
            return
        percent = min(percent,99)
        if not b_allow_regression and percent < self._progress_percent:
            return
        self._progress_percent = percent
        self._notify_observers(b_progress=True, b_allow_regression = b_allow_regression)
        
    def progress_caller(self, increment):
        self.caller_progress_increment = increment
        return self 
        
    def progress_caller_to(self, to):
        self.caller_progress_to = to
        return self 

    def is_set(self):
        return self._is_set

    def is_error(self):
        return self._exc is not None

    def get_error(self):
        assertions.fail_unless(self.is_error(),"get_error called, but there is no error")
        return self._exc

    def get_val_or_error(self):
        assertions.fail_unless(self.is_set(),"get_val_or_error called, but future is not set")
        return self._val,self._exc

    def wait(self,timeout=None):
        if self.is_set():
            return
        
        if self._event is None:
            with self._lock:
                if self.is_set():
                    return
                if self._event is None:
                    self._event = threading.Event()           
            
        if timeout is None:
            self._event.wait()
        else:
            self._event.wait(timeout/1000.0)
            b_signaled = self._event.is_set()
            if not b_signaled:
                raise FutureTimeoutException("Future not ready by timeout")
        assertions.fail_unless(self.is_set(),"Future is not ready after wait")
    
    def get(self,timeout=None):
        """If timeout is not None, it should be the maximum time to wait (in milliseconds). If the future isn't ready
           by this time, the method will raise FutureTimeoutException.
           NOTE: If get is called for a future that has attached observers, then order is not guaranteed between them. 
                 i.e. get() may return before observers are called (or while they are running)
                 Also note that if future was set with an error, get will re-throw the exception in the caller's thread.
        """
        self.wait(timeout=timeout)
        if self.is_error():
            raise self._exc
        return self._val
    
    def get_progress(self):
        # Cannot synchronize this method, since it can create deadlocks in complex scenarios 
        # Example: 
        #       when AggregateFuture used to call get_progress for all child_futures on each progress update of one of them,
        #       then trying to update two child futures from two different threads would cause a deadlock. both threads would
        #       acquire respective mutex on their futures, and then try to update aggregator. Since aggregator update is synchronized,
        #       then the first thread would get the mutex and the second one would wait (while holding the mutex on its future).
        #       Now the first thread tries to get progress from second future and we have a deadlock.
        #       AggregateFuture no longer acts this way, but other scenarios could do similar things, so it is 
        #       safer to only synchronize on "write" methods and not on "read".
        # Instead we guarantee a consistent result by double checking whether future is set, and rely on fact that future can only be set once,
        # and is immutable once it is set.
        first_is_set = self.is_set()
        is_error = self.is_error()
        percent = self._progress_percent
        is_set = self.is_set()
        if is_set != first_is_set:
            is_error = self.is_error()
            percent = self._progress_percent
        if is_error:
            error = self.get_error()
        else:
            error = None            
        return ProgressDetails(is_set,percent,error)

    def get_frozen_value(self):
        progress = self.get_progress()
        if progress.is_set and not progress.is_error:
            value = self.get()
        else:
            value = None
        return FutureValue(value, progress)

    @staticmethod
    def preset(val):
        '''Convenience method, that returns a future that is preset with the value val.'''
        f = Future().set_name('preset')
        f.set(val)
        return f

    @staticmethod
    def preset_error(exc):
        '''Convenience method, that returns a future that is preset with given exception.'''
        f = Future().set_name('preset_error')
        f.set_error(exc)
        return f

    def track_future(self, observed_future, b_chain_progress = True):
        """ Make this future track another future. This is different from chain_progress since we assume there is a single
            future to depend on so this future is set when the other is set with the same value.
        """
        observed_future.attach_observer(self.track_future_callback, b_notify_on_progress = b_chain_progress)
    
    def track_future_callback(self, f, 
                              **kw): #@UnusedVariable
        if self.is_set():
            return
        progress = f.get_progress()
        if progress.is_set:
            if progress.error:
                self.set_error(progress.error)
            else:
                self.set(f.get())
        else:
            self.set_progress(progress.percent,b_allow_regression = True)
    
    def chain_progress(self, observed_future, progress_mapping=(0,100)):
        """Convenience method that makes this future observe progress on another future, and sets progress from that
           future "as is" into this one.
        """
        start, end = progress_mapping
        ratio = (end - start)/100.0
        observed_future.attach_observer(partial(self.chain_progress_callback, start=start, ratio=ratio), b_notify_on_progress=True)

    def chain_progress_callback(self, observed_future, start=0, ratio=1.0, b_allow_regression=False, 
                                **kw): #@UnusedVariable
        if self.is_set():
            return
        progress = observed_future.get_progress()
        new_progress = start + int(ratio * progress.percent)
        self.set_progress(new_progress,b_allow_regression = b_allow_regression)
       
    def add_timeout(self, timer_manager, timeout):
        def update_timeout():
            """ sets the future due to timeout. future might be already set """
            if self.is_set():
                return
            self.set_error(FutureTimeoutException('added timeout has expired, timeout = %s' % timeout))
        timer = timer_manager.get_timer(update_timeout, timeout, True)
        self.attach_observer(partial(self._cancel_timer, timer))
        return self
    
    def _cancel_timer(self,
                      timer,
                      f, #@UnusedVariable
                      **kw): #@UnusedVariable
        timer.cancel() # can deal with already canceled
    
    def start_auto_progress(self, timer_manager, timeout, update_period):
        one_progress = 100 * update_period / timeout 
        def update_progress():
            """ sets the future's progress """
            if self.is_set():
                timer.cancel()
                return
            self.set_progress(self._progress_percent + one_progress)
        
        timer = timer_manager.get_timer(update_progress, update_period, False) 
        self.attach_observer(partial(self._cancel_timer,timer))
        return self
    
    
############################
# FutureAggregator
############################
class FutureAggregator(object):
    '''Used to wait for completion of several futures. The class is used as follows:
       1) futures are added by calling add_future() method
       2) after all futures are added, call activate() to get the aggregate future
       3) when all futures are set, the class will set the aggregate future. by default it will be set with the list of all 
          values from sub-futures waited on (but user can provide value aggregator - see ctor for details)

       if one or more of the futures is set with an error, the aggregate future will also be in error state.
       in that case the error will hold the exception from one of the errors set. The aggregate future
       will still only be set (with error) once all the futures are set.

       the aggregate future supports progress - the progress is the average progress of all sub-futures
    '''
    @staticmethod
    def default_value_aggregator(values):
        return values

    def __init__(self, value_aggregator=None):
        '''value_aggregator, if provided is called with list of values from sub-futures, and should return the aggregate result'''
        self._lock = RLock() # used by @synchronized() decorator
        self._futures = []
        self._result = Future().set_name('FutureAggregator')
        self._n_not_set_yet = None
        self._dct_progress = None
        if value_aggregator is None:
            self._value_aggregator = FutureAggregator.default_value_aggregator
        else:
            self._value_aggregator = value_aggregator

    @synchronized()
    def get_size(self):
        return len(self._futures)

    @synchronized()
    def add_future(self,f):
        assertions.fail_unless(self._n_not_set_yet is None, "Future added after activation")
        assertions.fail_unless(isinstance(f,Future), "f is not a future (did you forget using 'self._ao.func() ?)", f=f)
        self._futures.append(f)

    @synchronized()
    def activate(self):
        if not self._futures: # handle boundary case of 0 futures
            self._set_result()
        else:
            self._n_not_set_yet = len(self._futures)
            self._dct_progress = dict((f,0) for f in self._futures)
            for f in self._futures:
                f.attach_observer(self._notify_future_change,b_notify_on_progress=True)
        return self._result

    @synchronized()
    def _notify_future_change(self,
                              f,
                              **kw): #@UnusedVariable
        progress = f.get_progress()
        if progress.is_set:
            self._n_not_set_yet -= 1
            if self._n_not_set_yet == 0:
                self._set_result()
                return # don't update progress if result was set

        # update progress
        self._dct_progress[f] = progress.percent
        pct = sum(self._dct_progress.itervalues()) / len(self._futures) # NOTE: return int, not float! (C# type assumption)
        self._result.set_progress(pct)

    @synchronized()
    def _set_result(self):
        for f in self._futures:
            assertions.fail_unless(f.is_set(), "_set_result called, but at least one future not set yet")
        for f in self._futures:
            if f.is_error():
                self._result.set_error(f.get_error())
                return
        agg_val = self._value_aggregator( [f.get() for f in self._futures] )
        self._result.set(agg_val)

############################
# FutureAny
############################
class FutureAny(object):
    '''Used to wait for completion of one of several futures. The class is used as follows:
       1) futures are give in the ctor, or added with add_future()
       2) call activate() to get the aggregate future
       3) when one of the futures is set, the class will set the aggregate future with the corresponding result/error.

       the aggregate future supports progress:
          before it is set, the progress is the max progress of all sub-futures.
          after it is set, the progress is equivalent to a normal future set to same value/error.
    '''
    def __init__(self, *futures):
        self._lock = RLock() # used by @synchronized() decorator
        self._futures = []
        self._result = None
        for f in futures:
            self.add_future(f)

    @synchronized()
    def add_future(self,f):
        assertions.fail_unless(self._result is None, "Future added after activation")
        assertions.fail_unless(isinstance(f,Future), "f is not a future", f=f)
        self._futures.append(f)

    @synchronized()
    def activate(self):
        assertions.fail_unless(self._futures, "Tried to use FutureAny without any futures")
        assertions.fail_unless(self._result is None, "FutureAny is already activated")
        self._result = Future().set_name('FutureAny')
        for f in self._futures:
            f.attach_observer(self._notify_future_change,b_notify_on_progress=True)
        return self._result

    @synchronized()
    def _notify_future_change(self,
                              f, 
                              **kw): #@UnusedVariable
        if self._result.is_set():
            return        
        progress = f.get_progress()
        
        # check if we can set the result
        if progress.is_set:
            if f.is_error():
                self._result.set_error(f.get_error())
            else:
                self._result.set(f.get())
            return

        # update progress if it's higher than current
        percent = progress.percent
        last_percent = self._result.get_progress().percent
        if percent > last_percent:
            self._result.set_progress(percent)

############################
# ProgressObserver
############################
class ProgressObserver(object):
    """ Helper class for an observer that calls a method every time the progress changes by a configurable amount
        update_method signature is: update_method(int p). where 0<=p<=100
        minimal_change_for_update is the minimal change required to call update_method from the last value it was called for.
        Note this observer can never go backwards in 
    """
    def __init__(self, update_method, minimal_change_for_update):
        self.last_reported_progress = None
        self.update_method = update_method
        self.minimal_change_for_update = minimal_change_for_update
    
    def __call__(self, f, **_):
        progress = f.get_progress().percent
        if (self.last_reported_progress is None)\
           or (progress - self.last_reported_progress >= self.minimal_change_for_update)\
           or (progress == 100 and self.last_reported_progress != 100):
            self.update_method(progress)
            self.last_reported_progress = progress
        
############################
# sleep_future
############################
def sleep_future(timer_manager, duration): # duration is in milliseconds
    f = Future().set_name('sleep_future')
    def set_f():
        f.set(None)
    timer_manager.get_timer(set_f, duration, True)
    f.start_auto_progress(timer_manager, duration, duration / 10)
    return f
