from infra.util import synchronized, RLock, fmt_exc, prehistory, total_milliseconds
from infra import assertions, log
from datetime import timedelta
import copy 

class TimerManager(object):

    def __init__(self,factory):
        self.factory = factory
        self.logger = log.get_class_logger(self)
        self._lock = RLock() # used by @synchronized() decorator
        self.clock = 0 # virtual time (in milliseconds)
        self._all_timers = set() # set of (expiry time, timer)
        self.time_start = prehistory + timedelta(days=365) # makes sure prehistory happens strictly before all other times

    def now(self):
        return self.time_start + timedelta(microseconds=self.clock*1000)

    def get_timer(self,*a,**kw):
        return Timer(self,*a,**kw)        

    @synchronized()
    def register(self, timer):
        assertions.fail_if(timer.interval<0, 'negative interval is illegal', interval=timer.interval)
        expiry = self.clock + (timer.interval if timer.b_one_time else 0)
        self._all_timers.add( (expiry,timer) )
        self._check_timers()

    @synchronized()
    def remove(self, timer):
        for e,t in copy.copy(self._all_timers):
            if t==timer:
                self._all_timers.remove((e,t))
        
    @synchronized()
    def remove_all(self):
        self._all_timers = set()

    def advance_time(self, delta): # delta can be timedelta or milliseconds
        if isinstance(delta, timedelta):
            delta = total_milliseconds(delta)
        self.clock += delta
        self._check_timers()

    def _check_timers(self):
        expired = [(e,t) for e,t in self._all_timers if e <= self.clock]
        self._all_timers = set([(e,t) for e,t in self._all_timers if e > self.clock])
        # handle repeaters
        for e,t in expired[:]: # go over copy, since we append to the original list during iteration
            if t.interval > 0 and not t.b_one_time:
                e += t.interval
                while e <= self.clock:
                    expired.append( (e,t) )
                    e += t.interval
                self._all_timers.add( (e,t) )

        # fire timers in order of expiry time
        expired.sort()
        for _,t in expired:
            t._fire()

    def cancel_all_timers(self):
        self.logger.Debug('Cancel_all called. cancelling %s timers' % (len(self._all_timers),))
        for _,t in list(self._all_timers):
            t.cancel()

    def TEST_get_all_timers(self):
        return self._all_timers
    
    def TEST_set_now(self, dt):
        self.clock = 0
        self.time_start = dt

class Timer(object):
    def __init__(self,timer_manager,f,interval,b_one_time,*a,**kw):
        self.timer_manager = timer_manager
        self.logger = self.timer_manager.logger
        self.f = f
        self.interval = interval
        self.b_one_time = b_one_time
        self.a = a
        self.kw = kw
        self.timer_manager.register(self)
        self.logger.Debug('Created timer with f=%s, interval=%s, b_one_time=%s, a=%s, kw=%s' % (f,interval,b_one_time,a,kw))

    def __str__(self):
        return "Timer(f=%s,a=%s,kw=%s)" % (self.f,self.a,self.kw)

    def __repr__(self):
        return "Timer(f=%s,a=%s,kw=%s)" % (self.f,self.a,self.kw)

    def _fire(self):
        self.logger.Debug('Timer fired. f=%s, a=%s, kw=%s' % (self.f,self.a,self.kw))
        try:
            self.f(*self.a, **self.kw)
        except Exception,e:
            assertions.warn('Got exception in timer invocation. f=%s, a=%s, kw=%s, exc=%s' % (self.f,self.a,self.kw,fmt_exc(e)))

    def cancel(self):
        self.logger.Debug('Timer cancelled. f=%s, a=%s, kw=%s' % (self.f,self.a,self.kw))
        self.timer_manager.remove(self)

