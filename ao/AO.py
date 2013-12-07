import Queue
from dynamic_proxy import DynamicProxy
from util import fmt_exc
from DTO import DTO, Bunch
from null_object import NullObject
from future import Future
import assertions
import log
from threading import Thread, RLock
from types import GeneratorType
import random
from functools import partial
import inspect
from enum import Enum
import traceback
import sys
class AOException(Exception):
    pass

# NOTE: If an error hasn't occurred before Commit stage, then Commit is allowed to throw an exception and that exception will 
#       be set as the methods result.
#       If there was an error in the method body before reaching Commit, then Commit isn't allowed to throw an exception.
#       All other stages are not allowed to throw exceptions.

MethodCallStage = Enum('MethodCallStage', ['Request', 'Enter', 'Suspend', 'RequestResume', 'Resume', 'Commit', 'Exit'])
MethodCallType = Enum('MethodCallType', ['Sync', 'Async', 'Coroutine'])
RunStage = Enum('RunStage', ['AO_Stop', 'AO_Start', 'Start', 'Exception', 'Exit']) #@ReservedAssignment

def async_coroutine(f):
    '''decorator which marks f as a coroutine'''
    f.call_type = MethodCallType.Coroutine
    return f

def is_sync(f):
    '''decorator which marks f as synchronous (pass calls through directly to passive object)'''
    f.call_type = MethodCallType.Sync
    return f

def sync_facade(f):
    '''decorator which marks f as "sync facade" this means it is implemented as async (or coroutine)
       but appears to clients as sync, because it blocks until the result is ready'''
    f.sync_facade = 1
    return f

def get_sync_methods(cls):
    """ return methods that are either sync or sync_facade for the given class
    """
    if not cls:
        return set()
    def predicate(obj):
        return inspect.ismethod(obj) and (getattr(obj, 'call_type', None) == MethodCallType.Sync or getattr(obj, 'sync_facade', None) == 1)
    return set(item[0] for item in inspect.getmembers(cls,predicate))

def wrap_with(wrapper_func):
    '''decorating f with @wrap_with(w) will add w to list of wrappers over f.
       Running the wrappers is handled by the AO'''
    def deco(f):
        if hasattr(f,'wrappers'):
            wrapped_name = f.wrappers[-1].name
        else:
            f.wrappers = []
            wrapped_name = f.__name__
        wrapper_name = wrapper_func.__name__
        name = '%s(%s)' % (wrapper_name,wrapped_name)
        wrapper_modifiers = getattr(wrapper_func, 'wrapper_modifiers', {})
        wrapper_info = Bunch(callable=wrapper_func, name=name, base_name=f.__name__, wrapper_name=wrapper_name, wrapper_modifiers=wrapper_modifiers)
        f.wrappers.append(wrapper_info)
        return f
    return deco

class AsyncRV(DTO):
    '''Used to indicate a return value from an async coroutine'''
    def __init__(self,val):
        super(AsyncRV,self).__init__(locals())

class BaseAO(DynamicProxy):
    '''Base logic for active object that is shared between different implementations such as normal AO and
       SatelliteAO.
    '''        
    def __init__(self, passive_obj, factory=None):
        DynamicProxy.__init__(self)
        
        # configure hooks from factory if provided
        hook_config = getattr(factory, 'config', None) 
        self.method_call_hook = getattr(hook_config, 'AO_method_call_hook', NullObject())
        self.dct_run_hooks = getattr(hook_config, 'AO_dct_run_hooks', {}) # hook_name -> hook (so different ones don't override each other, but same ones do) 
        self.thread_start_hook = getattr(hook_config, 'AO_thread_start_hook', NullObject())
        
        assertions.assert_that(passive_obj is not None, "AO obj cannot be None", ao=self)
        self.obj = passive_obj
        self.obj._ao = self # allow passive object to make async calls to itself (and be aware of AO in general)
        self.id = random.getrandbits(63)
        self.is_active = False

        if hasattr(self.obj, 'logger'):
            logger_name = self.obj.logger.name
            self.logger = log.get_logger(logger_name+'.AO', b_raw_name=True)
        else:
            assertions.fail('Object wrapped as AO must have a logger. No logger found for passive object %s' % (self,))

        if hasattr(self.obj, 'name'):
            self.name = self.obj.name
        else:
            self.name = type(self.obj).__name__
            
    def __str__(self):
        return "%s(%s)" % (type(self).__name__, type(self.obj).__name__)
    
    def __dir__(self):
        ao_members = dir(self.__class__) + self.__dict__.keys()
        obj_public_methods = [name for name,val in self.obj.__class__.__dict__.iteritems() if callable(val) and not name.startswith('_')]
        return list(set(ao_members + obj_public_methods)) # unify and remove duplicates
    
    def run_hook(self, *a, **kw):
        for hook in self.dct_run_hooks.itervalues():
            hook(*a, **kw)

    def start(self):
        self.logger.Info("AO started")
        # If self.obj has start method, call it
        obj_start = getattr(self.obj, 'start', None)
        if callable(obj_start):
            try:
                obj_start()
            except Exception, e:
                assertions.warn('Got exception while starting AO. %s' % fmt_exc(e))
                raise
        self.is_active = True

    def quit(self): #@ReservedAssignment
        self.logger.Info("AO stopped (quit called)")
        # If self.obj has quit method, call it
        try:
            if self.is_active:
                obj_quit = self.obj.quit
                if callable(obj_quit):
                    try:
                        obj_quit()
                    except Exception, e:
                        assertions.warn('Got exception while quitting AO. %s' % fmt_exc(e))
        except AttributeError:
            pass # no quit method        
        self.logger.Debug('user quit hook finished')
        self.is_active = False
        
    @staticmethod
    def checkpoint(name):
        """Syntactic sugaring for declaring hook points 
        """
        return Future.preset(None).set_name(name)
        
    @staticmethod
    def progress_caller(increment):
        """Syntactic sugaring for progressing caller without doing anything
        """
        return Future.preset(None).progress_caller(increment)
        
    @staticmethod
    def progress_caller_to(endpoint):
        """Syntactic sugaring for progressing caller to endpoint without doing anything
        """
        return Future.preset(None).progress_caller_to(endpoint)

    def _get_callable(self,base_method,wrapper_level):
        """Gets the callable for the dispatch operation
           This is either the base_method or a wrapper of it indicated by wrapper_level.
           Return value is a pair: (callable,wrapper_info). wrapper_info is None if callable is not a wrapper.
        """
        # check if we should return a wrapper instead (and which one)
        wrappers = getattr(base_method,'wrappers',[])
        if wrapper_level is None:
            wrapper_level = len(wrappers)-1
        if wrapper_level < 0:
            return base_method,None

        # it's a wrapper call - build up a replacement for the original mth:

        # get the basic wrapper callable
        wrapper_info = wrappers[wrapper_level] 
        # prepare callable that will be passed to raw_wrapper as way to call the next level down
        next_level = wrapper_level-1
        def next_level_callable(*a,**kw): 
            return self._internal_invoke(base_method,a,kw,next_level)
        if next_level < 0:
            next_level_callable.__name__ = base_method.__name__
        else:
            next_level_callable.__name__ = wrappers[next_level].name
        next_level_callable.base_method = base_method
        next_level_callable.base_name = base_method.__name__

        # the actual replacement for base_method
        def wrapper(*a,**kw): 
            return wrapper_info.callable(
                self.obj, # provide the passive object as 'self' (looks like we're a method on the original object)
                next_level_callable, # provide a way to call the next level down
                *a,**kw) # the original arguments
        wrapper.__dict__.update(wrapper_info.callable.__dict__)
        wrapper.__name__ = wrapper_info.name
        wrapper.call_type = MethodCallType.Coroutine  # wrapper methods are always async_coroutines
        

        return wrapper,wrapper_info

    def _internal_invoke(self,method,a,kw,wrapper_level=None):
        method,wrapper_info = self._get_callable(method,wrapper_level)
        AO_cmd_meta_data = kw.pop('AO_cmd_meta_data',{})
        call_type = getattr(method,'call_type',MethodCallType.Async)
        f = Future()
        cmd = BaseAO.Cmd(call_type,f,self,method,a,kw,wrapper_info,AO_cmd_meta_data)
        f.set_name(cmd.qualified_name_no_wrappers)

        if call_type == MethodCallType.Sync: # ignores queue and executes immediately + blocks
            cmd()
            return f.get()
        else:
            self.enq(cmd)
            if hasattr(method,'sync_facade'): # does not ignore the queue but blocks
                return f.get()
            else:
                return f

    def AO_invoke(self,method,*a,**kw):
        return self._internal_invoke(method,a,kw)

    def _dispatch(self,dynamic_proxy_method_name,*a,**kw):
        """Called by DynamicProxy mechanism when a "proxied" method is called on the AO"""
        method = getattr(self.obj,dynamic_proxy_method_name)
        return self._internal_invoke(method,a,kw)

    class Cmd(object):
        def __init__(self,call_type,future,ao,method,a,kw,wrapper_info,AO_cmd_meta_data):
            self.call_type = call_type
            self.future = future
            self.inner_future = Future().set_name("AO Cmd inner future")            
            self.ao = ao
            self.logger = self.ao.logger
            self.method = method
            self.a = a
            self.kw = kw
            self.wrapper_info = wrapper_info
            self.AO_cmd_meta_data = AO_cmd_meta_data

            self.method_name = method.__name__
            self.invocation_id = '%s.%s-%s' % (self.ao.name,self.method_name,random.getrandbits(63))

            # used by coroutines
            self.coroutine = None
            self.yielded_future = None
            
            self.f_enter_hook = ao.method_call_hook(MethodCallStage.Request, self.call_type, self)

        @property
        def ao_name(self):
            return self.ao.name

        @property
        def ao_type_name(self):
            return type(self.ao.obj).__name__

        @property
        def qualified_name(self):
            return '%s.%s' % (self.ao_type_name,self.method_name)

        @property
        def qualified_name_no_wrappers(self):
            return '%s.%s' % (self.ao_type_name,self.base_method_name)
        
        @property
        def base_method_name(self):
            if self.wrapper_info is None:
                return self.method_name
            else:
                return self.wrapper_info.base_name

        @property
        def wrapper_name(self):
            return getattr(self.wrapper_info,'wrapper_name',None)

        def __str__(self):
            return 'Cmd(%s,%s,a=%s,kw=%s)' % (self.ao,self.invocation_id,self.a,self.kw)

        def __call__(self):
            self._apply_hook(
                future_hook = self.f_enter_hook, 
                func_set_result = self.set_result,
                func_continue = self.run,
                stage_entered = MethodCallStage.Enter,
            )
                        
        def run(self):
            if self.call_type == MethodCallType.Coroutine:
                try:
                    self.coroutine = self.method(*self.a, **self.kw) # get generator
                    assertions.fail_unless(isinstance(self.coroutine, GeneratorType),'Declared Co-Routine is not a generator', name=self.method_name, coroutine=self.coroutine)
                except Exception, e:
                    print "@@@Ido Cmd.run- setting trace (Coroutine)".format(**locals())
                    e.trace = traceback.format_exc()
                    self.set_result(exc = AOException('Got exception while getting Co-Routine - %s' % (fmt_exc(e),)))
                else:
                    self._step_coroutine()
                    
            else: # Sync or Async method
                try:
                    res = self.method(*self.a, **self.kw) # execute the method
                except Exception, e:
                    print "@@@Ido Cmd.run- setting trace Sync or Async method".format(**locals())
                    e.trace = traceback.format_exc()
                    self.set_result(exc = e)
                else:                        
                    self.set_result(val = res)

        def set_result(self,val=None,exc=None):                       
            assertions.fail_if(self.inner_future.is_set(),"in Cmd.set_result - inner future already set",cmd=self)
            if exc is not None:
                self.inner_future.set_error(exc)

            try:
                self.ao.method_call_hook(MethodCallStage.Commit,self.call_type,self)
            except Exception, e:
                if exc is None:
                    exc = e
                    self.inner_future.set_error(exc)

            if exc is None:
                self.inner_future.set(val)

            f_hook = self.ao.method_call_hook(MethodCallStage.Exit,self.call_type,self)
            self._apply_hook(
                future_hook = f_hook, 
                func_set_result = self.future.set_val_or_error,
                func_continue = partial(self.future.set_by_other_future_value,self.inner_future),
                stage_entered = None,
            )
            
        def _apply_hook(self, future_hook, func_set_result, func_continue, stage_entered):
            if not future_hook: 
                future_hook = Future.preset(None).set_name('AO empty future hook')
            def completion(future_hook):
                if stage_entered != None:
                    self.ao.method_call_hook(stage_entered,self.call_type,self)                    
                val,exc = future_hook.get_val_or_error()
                if exc is not None:
                    func_set_result(exc=exc)
                elif isinstance(val,AsyncRV):
                    func_set_result(val=val.val)
                else:
                    assertions.fail_unless(val is None, "Hook returned a value, but not through AsyncRV", val=val)
                    func_continue()
                    
            if self.call_type == MethodCallType.Coroutine:
                future_hook.attach_observer(partial(self._async_completion,stage_entered,completion)) # Coroutine - don't block AO thread while waiting for hook's future
            else:
                future_hook.wait()
                completion(future_hook)
         
        def _async_completion(self, stage_entered, completion,future_hook, **_):
            b_entering = (stage_entered != None)
            if b_entering: 
                # perform next step from AO's thread, instead of thread setting the hook's future
                self.ao.enq(partial(completion,future_hook))
            else: 
                # shouldn't be any requirement about which thread performs the action when exiting
                # no need to go through the queue another time
                completion(future_hook)
                
        def _step_coroutine(self, val=None, exc=None):
            self.yielded_future = None
            etype = value = tb = None
            try:
                if exc is None:
                    yielded = self.coroutine.send(val)
                else:
                    etype, value, tb = sys.exc_info()
                    yielded = self.coroutine.throw(exc, traceback=tb)
                
                if isinstance(yielded,AsyncRV):
                    self.set_result(val=yielded.val)
                elif isinstance(yielded,Future):
                    self._handle_coroutine_suspend(yielded)
                else:
                    msg = 'Co-Routine {name} yielded unsupported type - {type}'.format(name=self.method, type=(type(yielded).__name__))
                    self.set_result(exc = AOException(msg))
            except StopIteration:
                self.set_result(exc = AOException("Co-Routine ended without AsyncRV"))
            except Exception, e:
                print "@@@Ido Cmd._step_coroutine- setting trace".format(**locals())
                e.trace = traceback.format_exc()
                print "@@@Ido Cmd._step_coroutine- e.trace={e.trace}".format(**locals())
                self.set_result(exc = e)
            finally:
                etype = value = tb = None
                

        def _handle_coroutine_suspend(self, yielded_future):
            self.yielded_future = yielded_future
            self.ao.method_call_hook(MethodCallStage.Suspend,MethodCallType.Coroutine,self)
            
            # chain progress if progress_mapping option selected
            if yielded_future.caller_progress_increment is not None:
                assertions.fail_unless(yielded_future.caller_progress_to is None, "You are combining two progress methods...")                
                parent_progress = self.future.get_progress().percent
                self.future.chain_progress(yielded_future, (parent_progress, parent_progress + yielded_future.caller_progress_increment))
                
            elif yielded_future.caller_progress_to is not None:
                assertions.fail_unless(yielded_future.caller_progress_increment is None, "You are combining two progress methods...")
                parent_progress = self.future.get_progress().percent
                self.future.chain_progress(yielded_future, (parent_progress, yielded_future.caller_progress_to))
                
            # attach observer for resuming the coroutine when future is set
            yielded_future.attach_observer(self.completion_callback)

        def completion_callback(self, wait_future,**_kw):
            f_hook = self.ao.method_call_hook(MethodCallStage.RequestResume, MethodCallType.Coroutine, self)
            val,exc = wait_future.get_val_or_error()
            self._apply_hook(
                future_hook = f_hook, 
                func_set_result = self._step_coroutine,
                func_continue = partial(self._step_coroutine,val,exc),
                stage_entered = MethodCallStage.Resume,
            )
            
class AO(BaseAO):
    '''A standard AO with one or more threads of execution'''
    def __init__(self, passive_obj, n_threads=1, factory=None):
        BaseAO.__init__(self, passive_obj, factory)
        self.q = Queue.Queue()
        self.n_threads = n_threads
        self.threads = []
        self.thread_start_hook_lock = RLock(); # A lock to protect the start hook calls

    def start(self, b_background=True):
        # make sure the AO is not running
        if self.threads:
            raise Exception("Cannot start an AO that is already running")
        BaseAO.start(self)
        self.run_hook(RunStage.AO_Start, ao=self)
        # start the threads
        for i in xrange(self.n_threads):
            t = Thread(target = self._run)
            if b_background:
                t.setDaemon(True)
            with self.thread_start_hook_lock: # serialize calls, so the hook doesn't have to be thread safe
                self.thread_start_hook(ao=self, thread=t, thread_number=i, b_before_starting_thread=True)
            self.threads.append(t)
            t.start()

    def _run(self):
        with self.thread_start_hook_lock:
            self.thread_start_hook(ao=self, thread=None, thread_number=None, b_before_starting_thread=False)
        self.run_hook(RunStage.Start)
        while True:
            cmd = self.q.get()
            try:
                rc = cmd()
                if rc:
                    break
            except Exception, e:
                #print('Uncaught Exception: %s' % fmt_exc(e))
                assertions.warn('Uncaught Exception:',ao=self, details=fmt_exc(e))
                self.run_hook(RunStage.Exception)
        self.run_hook(RunStage.Exit)

    def enq(self,cmd):
        self.q.put(cmd)

    def qsize(self):           
        return self.q.qsize()

    def quit(self, b_blocking=True): #@ReservedAssignment
        f_done = Future()
        def async_quit():            
            # ask all threads to exit
            def finish():
                self.logger.Debug('quiting AO thread')
                return 1
            for _ in xrange(self.n_threads):
                self.enq(finish)
            
            # wait for them
            for t in self.threads:
                t.join()
                
            # run passive object's quit method and hook
            BaseAO.quit(self)
            self.run_hook(RunStage.AO_Stop,ao=self)
            
            # signal we're done
            self.logger.Debug('quit finished')            
            f_done.set(None)
                        
        t = Thread(target = async_quit)
        t.setDaemon(True)
        t.start()
        
        if b_blocking:
            f_done.get()
        else:
            return f_done
        
    def _visit_all_threads(self, mth):
        """Allows running a given method once in every one of the AO threads.
           The method returns a future that is set by the last thread after executing the method. 
           The future's value is the return value from the call to mth by the last thread.  
        """ 
        class Visitor(object):
            def __init__(self,n_threads,ao, mth):
                self.lock = RLock()
                self.finished = Future().set_name('AO Visitor')
                self.n_visits = 0
                self.n_threads = n_threads
                self.ao = ao
                self.mth = mth

            def visit(self):
                """ each thread will execute exactly one visit call """
                with self.lock:
                    self.n_visits += 1
                    b_last = (self.n_visits == self.n_threads)
                    rc = mth()
                if b_last:
                    self.finished.set(rc)
                    
                # This blocks the thread until we're done with all threads
                # It's necessary so we don't dequeue another thread's visit command
                # It also ensures that commands enqueued after visit started don't start executing until it's finished
                # which makes visit act in a quiesced state.
                self.finished.get()

        visitor = Visitor(self.n_threads,self, mth)
        for _ in xrange(self.n_threads):
            self.enq(visitor.visit)
        return visitor.finished

    def AO_reset_queue(self):
        """Removes all current commands waiting in the queue"""
        self.q = Queue.Queue()

    def flush(self):
        """Returns future that is set when all methods in AO's queue have returned.
           The future's value is set with number of items in the queue that were added after flush was started.
           Should be implemented differently for subclasses. Common behavior goes here.           
        """
        def visitor_method():
            return self.qsize()
        f_visit = self._visit_all_threads(visitor_method)
        return f_visit

    def TEST_complete_flush(self, single_timeout=None, max_iterations=None, b_allow_incomplete=False):
        """
        returns when the AO queue is empty.
        this is a good function to use in tests when you are waiting for AO actions to complete. 
        NOTE: this will not work if any of the actions that you are waiting for depend on other actions\futures that are
        running outside of the same queue, because then your action can yield a future, the queue and threads will be empty,
        and some other entity will set the future and cause the action to resume after we have concluded that the queue is empty.
        for this reason, this function should be used in a context where actions in the queue depend only on other actions
        that belong to this AO (or its satellites), and are thus running in the same queue\threads.
        """
        if single_timeout is None:
            single_timeout = 10 * 1000
        if max_iterations is None:
            max_iterations = 10
        for _ in xrange(max_iterations):
            qsize = self.flush().get(single_timeout)
            if qsize == 0:
                return True
        if not b_allow_incomplete:
            raise Exception("%s still busy after %s iterations" % (self.name,max_iterations))
        return False

    def get_base_ao(self):
        return self

class SatelliteAO(BaseAO):
    '''An AO which doesn't have any threads, but instead uses the threads and command queues of a parent AO.
       Note that the parent_ao may itself be a SatelliteAO, in which case the command is enqued to its parent, 
       and so on.
    '''
    def __init__(self,passive_obj,parent_ao,factory=None):
        BaseAO.__init__(self,passive_obj,factory)
        self.parent_ao = parent_ao

    def enq(self,cmd):
        self.parent_ao.enq(cmd)

    def qsize(self):           
        return self.parent_ao.qsize()

    def flush(self):
        return self.parent_ao.flush()

    def get_base_ao(self):
        return self.parent_ao.get_base_ao()

    def TEST_complete_flush(self, *a, **kw):
        return self.parent_ao.TEST_complete_flush(*a,**kw)

class SyncFacade(DynamicProxy):
    '''Wraps an AO like object (an object that it's methods return futures) in a facade that 
       blocks on the result by calling get() on the returned futures.
       Note that if the future is set with error, then the SyncFacade will re-throw
       the original exception in the caller's thread.
    '''
    def __init__(self, wrapped, timeout = None):
        DynamicProxy.__init__(self)
        self._timeout = timeout
        self._wrapped = wrapped
        if hasattr(wrapped,'logger'):
            name = wrapped.logger.name + '.Sync'
            self.logger = log.get_logger(name)
        else:
            self.logger = log.get_logger('AO.Sync') # will propagate to root logger
            assertions.warn('%s - No logger found for %s' % (self,wrapped))

    @property
    def obj(self):
        return self._wrapped.obj # Using a property remains consistent when the _wrapped.obj changes
            
    def __str__(self):
        return "%s(%s)" % (type(self).__name__, self._wrapped)

    def __dir__(self):
        return dir(self._wrapped)
    
    def _dispatch(self,name_,*a,**kw):
        self.logger.Debug('ENTERing %s' % name_)
        try:
            method = getattr(self._wrapped,name_)
            rv = method(*a,**kw)
            if isinstance(rv,Future): # NOTE - this won't work with sync methods that return Future
                rv = rv.get(self._timeout)
            self.logger.Debug('%s EXITED normally' % name_)
            return rv
        except:
            self.logger.Debug('%s EXITED with exception' % name_) # we'll get a warning from the AO itself
            raise


