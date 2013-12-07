from test_infra_base import BackendInfraTest, PassiveObject, get_logger
import AO as AO
import assertions
from future import Future, FutureTimeoutException
from stopwatch import Stopwatch
import util
from dynamic_proxy import DynamicProxy
from mock_object.mock import Mock
import threading
from threading import Thread
import time
import gc
from AO import async_coroutine
from AO import AsyncRV

class TestException(Exception):
    pass        

class TestAOCommonSetup(BackendInfraTest):
    def setUp(self):
        super(TestAOCommonSetup,self).setUp()
        self.aos_to_stop = []

    def tearDown(self):
        for ao in self.aos_to_stop:
            ao.quit()

class TestAO(TestAOCommonSetup):
    def test_sanity(self):
        class A(PassiveObject):
            def __init__(self,name):
                super(A,self).__init__()
                self.name = name
            def repeat(self,n,msg):
                return '%s: %s' % (self.name, ', '.join(n*[msg]))
            def get_thread(self):
                return threading.current_thread()
        ao = AO.AO(A('bob'))
        ao.start()
        self.aos_to_stop.append(ao)

        val = ao.repeat(3,msg='hi').get()
        self.assertEqual(val,'bob: hi, hi, hi')

        self.assertEqual(str(ao),'AO(A)')

        # verify all calls to AO execute from its own thread
        main_thread = threading.current_thread()
        t_id = ao.get_thread().get()
        self.assertNotEqual(t_id, main_thread) # not from our thread
        t_id2 = ao.get_thread().get()
        self.assertEqual(t_id2, t_id) # all calls execute from same AO thread
        
    def test_double_start(self):
        class A(PassiveObject):
            pass
        ao = AO.AO(A())
        ao.start()
        self.aos_to_stop.append(ao)
        self.assertRaises(Exception, ao.start)

    def test_name(self):
        class B(PassiveObject):
            pass
        ao = AO.AO(B())
        self.assertEqual(ao.name,'B') # no explicit name - name comes from type

        class A(object):
            def __init__(self):
                self.logger = get_logger('Acme.A3.1')
                self.name = 'A3.One'
        ao = AO.AO(A())
        self.assertEqual(ao.name,'A3.One')
        
    def test_dir(self):
        class A(PassiveObject):
            def __init__(self):
                super(A,self).__init__()
                self.x = 0
            def start(self) : pass # helps test start doesn't appear twice
            def foo(self): pass
            def _private(self): pass
        ao = AO.AO(A())
        d = dir(ao)
        self.assert_('foo' in d, d)
        self.assert_('_private' not in d, d)
        self.assert_('obj' in d, d)
        self.assert_('start' in d, d) # this method is in A. should appear once
        self.assert_('quit' in d, d) # this method comes only from AO. should also appear
        
        # verify names are not duplicates
        self.assertEqual(len(d),len(set(d)),d)
        
    def test_future_name(self):
        def wrap_it(self,
                    wrapped): #@UnusedVariable
            yield AO.AsyncRV()

        class A(PassiveObject):
            def __init__(self,i):
                super(A,self).__init__()
                self.i = i

        @AO.wrap_with(wrap_it)
        class MyAO(PassiveObject):
            def __init__(self):
                super(MyAO,self).__init__()
                self.name = 'MyAO-3'
                
            @AO.wrap_with(wrap_it)
            def foo(self):
                pass
        ao = AO.AO(MyAO())
        
        f = ao.foo()
        self.assertEqual(f.name,'MyAO.foo')
        
    def test_invoke(self):
        class A(PassiveObject):
            pass

        ao = AO.AO(A())
        ao.start()
        self.aos_to_stop.append(ao)

        def add(x,y):
            return (x+y, id(threading.current_thread()))
        total,t_id = ao.AO_invoke(add,2,3).get()
        self.assertEqual(total,5)    
        self.assertNotEqual(t_id, id(threading.current_thread()))

        @AO.async_coroutine
        def wait_for_it(x,f):
            y = yield f
            yield AO.AsyncRV(x+y)
        f = Future.preset(3)            
        total = ao.AO_invoke(wait_for_it,2,f).get(1000)
        self.assertEqual(total,5)

    def test_passive_object_hooks(self):
        class Passive(PassiveObject):
            def start(self):
                self.ao_id = id(self._ao)
            def quit(self): #@ReservedAssignment
                self.b_quit = True

        p = Passive()        
        ao = AO.AO(p)
        ao.start()
        self.aos_to_stop.append(ao)

        self.assertEqual(p.ao_id,id(ao))
        ao.quit()
        self.assertEqual(p.b_quit,True)

    def test_n_threads(self):
        sleep_time = 0.1

        class Sleeper(PassiveObject):
            def __init__(self):
                super(Sleeper,self).__init__()
                self._lock = util.RLock() # used by @synchronized() decorator
                self.i = 0
                self.thread_ids = set()

            @util.synchronized()
            def _critical_section(self):
                self.thread_ids.add(id(threading.current_thread()))
                self.i += 1

            def sleep(self):
                time.sleep(sleep_time)
                self._critical_section()

        n_threads = 5
        n_calls = 100
        ao = AO.AO(Sleeper(),n_threads)
        ao.start()
        self.aos_to_stop.append(ao)

        s = Stopwatch()
        s.start()
        futures = [ao.sleep() for _ in xrange(n_calls)]
        for f in futures:
            f.get()
        duration = s.duration()
        expected = sleep_time*n_calls / float(n_threads)
        self.assert_(0.9*expected < duration < 1.3*expected, 'duration=%s, expected=%s' % (duration,expected))
        self.assertEqual(ao.obj.i,n_calls)
        self.assertEqual(len(ao.obj.thread_ids),n_threads)
        self.failIf(id(threading.current_thread()) in ao.obj.thread_ids)

    def test_satellite(self):
        class A(PassiveObject):
            def get_ids(self):
                return id(self),id(threading.current_thread())
        ao = AO.AO(A())
        ao.start()
        self.aos_to_stop.append(ao)
        sat = AO.SatelliteAO(A(),ao)
        sat.start()
        a1, t1 = ao.get_ids().get()
        a2, t2 = sat.get_ids().get()
        self.assertEqual(t1,t2)
        self.assertNotEqual(a1,a2)
        
    def test_is_active(self):
        class A(PassiveObject):
            pass
        ao = AO.AO(A())
        self.assertFalse(ao.is_active)
        ao.start()
        self.aos_to_stop.append(ao)
        self.assertTrue(ao.is_active)
        ao.quit()        
        self.assertFalse(ao.is_active)
        
        # satellite
        ao2 = AO.AO(A())
        ao2.start()
        self.aos_to_stop.append(ao2)
        sat = AO.SatelliteAO(A(),ao)
        self.assertFalse(sat.is_active)
        sat.start()
        self.assertTrue(sat.is_active)
        sat.quit()
        self.assertFalse(sat.is_active)        

    def test_run_hooks(self):                
        class A(PassiveObject):
            pass

        n_threads = 3
        ao = AO.AO(A(),n_threads)
        A_hook = Mock()
        B_hook = Mock()     
        ao.dct_run_hooks['A'] = A_hook # set the hook before calling start (otherwise it's pointless)
        ao.dct_run_hooks['B'] = B_hook # set the hook before calling start (otherwise it's pointless)
        ao.start()
        self.aos_to_stop.append(ao)
        
        ao._visit_all_threads(lambda: None).get() # make sure all threads have started
        for h in [A_hook, B_hook]:
            self.assertEqual(h.call_args_list,[
                ( (AO.RunStage.AO_Start,), {'ao' : ao} ),
                ( (AO.RunStage.Start,), {} ),
                ( (AO.RunStage.Start,), {} ),
                ( (AO.RunStage.Start,), {} ),
            ])
            h.reset()
            
        ao.quit()        
        for h in [A_hook, B_hook]:
            self.assertEqual(h.call_args_list,[
                ( (AO.RunStage.Exit,), {} ),
                ( (AO.RunStage.Exit,), {} ),
                ( (AO.RunStage.Exit,), {} ),
                ( (AO.RunStage.AO_Stop,), {'ao' : ao} ),
            ])        
            h.reset()

        ao.quit()        
        for h in [A_hook, B_hook]:
            self.assertEqual(h.call_args_list,[
                ( (AO.RunStage.AO_Stop,), {'ao' : ao} ),
            ])        
            h.reset()

    def test_thread_start_hook(self):                
        class A(PassiveObject):
            def get_thread(self):
                time.sleep(0.1)
                return threading.current_thread()

        # We iterate over the test 10 times to assure stability
        for _ in xrange(1,10):
            n_threads = 3
            ao = AO.AO(A(),n_threads)        
            ao.thread_start_hook = Mock() # set the hook before calling start (otherwise it's pointless)        
            ao.start()
            self.aos_to_stop.append(ao)
    
            def wait_condition(): self.assertEqual(ao.thread_start_hook.call_count,2*n_threads)
            self.wait_until_true(wait_condition)
    
            lst_calls_before_start = []
            for call_args in ao.thread_start_hook.call_args_list:
                args,kwargs = call_args
                self.assertEqual(args,())
                self.assertEqual(len(kwargs),4)
                self.assertEqual(kwargs['ao'],ao)
                if kwargs['b_before_starting_thread']:
                    lst_calls_before_start.append(kwargs)
                else:
                    self.assertEqual(kwargs['thread'],None)
                    self.assertEqual(kwargs['thread_number'],None)                
    
            lst_threads = []
            for i,kwargs in enumerate(lst_calls_before_start):
                    thread_obj = kwargs['thread']
                    self.assert_(isinstance(thread_obj, Thread), "expected a thread. got %s" % (thread_obj,))
                    lst_threads.append(thread_obj)
                    self.assertEqual(kwargs['thread_number'],i)                
            
            t = ao.get_thread().get(500)                
            self.assert_(t in lst_threads, "Unexpected thread. t=%s, lst_threads=%s" % (t,lst_threads))
                
            # now do the same with satellite - shouldn't get calls
            class Sat(PassiveObject):
                pass
            sat = Sat()
            sat = AO.SatelliteAO(sat,ao)
            sat.thread_start_hook = Mock()
            sat.start()        
            self.assertEqual(sat.thread_start_hook.called,False)
            
    def test_visit_all_threads(self):
        class A(PassiveObject):
            pass
        n_threads = 3
        ao = AO.AO(A(),n_threads)
        ao.start()
        
        lst_thread_ids = []
        def find_thread():
            thread_id = id(threading.current_thread())
            lst_thread_ids.append(thread_id)
            return thread_id
        f = ao._visit_all_threads(find_thread)
        last_thread_id = f.get(5000)
        
        self.assertEqual(len(lst_thread_ids), n_threads) # verify method ran exactly n_threads times
        self.assertEqual(len(set(lst_thread_ids)), n_threads) # verify it ran once in each thread
        self.assertEqual(last_thread_id, lst_thread_ids[-1]) # verify return value is what we got back from mth on the last thread 
        
    def _test_quit(self, b_blocking):
        class A(PassiveObject):
            def get_thread(self):
                time.sleep(0.1)
                return threading.current_thread()
        n_threads = 3
        ao = AO.AO(A(),n_threads)
        ao.start()

        futures = [ao.get_thread() for _ in xrange(n_threads)]
        threads = [f.get() for f in futures]
        for t in threads:
            self.failUnless(t.is_alive())
        if b_blocking:
            ao.quit()
        else:
            f_quit = ao.quit(b_blocking=False)
            f_quit.get()
        for t in threads:
            self.failIf(t.is_alive())

    def test_quit(self):
        self._test_quit(b_blocking=True)

    def test_quit_async(self):
        self._test_quit(b_blocking=False)
        
    def test_double_quit(self):
        class A(PassiveObject):
            pass
        ao = AO.AO(A())
        ao.start()
        ao.quit()
        ao.quit() # 2nd quit should be NOP

    def test_flush(self):
        class A(PassiveObject):
            def long_op(self,f):
                time.sleep(1)
                f.set(None)
        n_threads = 3
        ao = AO.AO(A(),n_threads)
        ao.start()
        self.aos_to_stop.append(ao)

        class Sat(PassiveObject): pass
        sat = AO.SatelliteAO(Sat(),ao)

        def flush_and_check(obj,timeout):
            s = Stopwatch()
            futures = []
            for _ in xrange(n_threads-1): # all threads except for one will be busy when flush is called
                f = Future()
                futures.append(f)
                ao.long_op(f)

            s.start()
            obj.flush().get(timeout)
            duration = s.duration()

            for f in futures:
                self.assert_(f.is_set(),"long_op didn't end after flush")
            self.assert_(0.9 < duration < 1.3, "Operation took unexpected time. duration=%s" % (duration,))

        flush_and_check(ao,3000)
        flush_and_check(sat,3000)
        flush_and_check(ao,None)
        self.assertRaises(FutureTimeoutException, flush_and_check,ao,1)
        self.assertRaises(FutureTimeoutException, flush_and_check,sat,1)

    def test_reset_queue(self):
        class A(PassiveObject):
            def append(self,lst,x):
                lst.append(x)

        # baseline - without reset                
        lst = []                
        ao = AO.AO(A())
        ao.append(lst,1)
        ao.start()
        self.aos_to_stop.append(ao)
        ao.append(lst,2).get()
        self.assertEqual(lst,[1,2])

        # with reset - see that first command is not executed
        lst = []                
        ao = AO.AO(A())
        ao.append(lst,1)
        ao.AO_reset_queue()
        ao.start()
        self.aos_to_stop.append(ao)
        ao.append(lst,2).get()
        self.assertEqual(lst,[2])

    def test_coroutine(self):
        sleep_time = 0.1
        class Worker(PassiveObject):
            def add(self,x,y):
                time.sleep(sleep_time)
                return x+y

        class Main(PassiveObject):
            def __init__(self,worker_ao):
                super(Main,self).__init__()
                self.worker_ao = worker_ao

            @AO.async_coroutine
            def sum(self,n): #@ReservedAssignment
                total = 0
                for i in xrange(n):
                    total = yield self.worker_ao.add(total,i)
                yield AO.AsyncRV(total)

        n_worker_threads = 4
        worker_ao = AO.AO(Worker(),n_worker_threads)
        worker_ao.start()
        self.aos_to_stop.append(worker_ao)

        main_ao = AO.AO(Main(worker_ao))
        main_ao.start()
        self.aos_to_stop.append(main_ao)

        stopwatch = Stopwatch()
        stopwatch.start()
        n = 10
        futures = [main_ao.sum(n) for _ in xrange(n_worker_threads)]
        sums = [f.get() for f in futures]
        duration = stopwatch.duration()
        expected = n*sleep_time # coroutine allows us to work in parallel with all Worker threads from single Main thread
        self.assert_(0.9*expected < duration < 1.8*expected, 'duration=%s' % duration)
        for s in sums:
            self.assertEqual(s,sum(range(n)))

    def test_exception(self):
        class Bad(PassiveObject):
            @async_coroutine
            def bad(self):
                e = Exception("I'm a bad class")
                raise e
                yield AsyncRV(None)
            @async_coroutine
            def bad_async(self):
                res = yield self._ao.bad()
                yield AsyncRV(res)
                
        ao = AO.AO(Bad())
        ao.start()
        self.aos_to_stop.append(ao)

        f = ao.bad()
        f.get()
        self.assertRaises(Exception,f.get)
        self.assertEquals(f.is_error(),True)
        self.assertEquals(str(f.get_error()),"I'm a bad class")

    def test_coroutine_exception(self):
        class Worker(PassiveObject):
            def bad(self,i):
                if i>1:
                    raise Exception('BAD %s' % i)

        class Main(PassiveObject):
            def __init__(self,worker_ao):
                super(Main,self).__init__()
                self.worker_ao = worker_ao

            @AO.async_coroutine
            def use_bad(self,n):
                for i in xrange(n):
                    yield self.worker_ao.bad(i)
                yield AO.AsyncRV("Won't get here")

        worker_ao = AO.AO(Worker())
        worker_ao.start()
        self.aos_to_stop.append(worker_ao)

        main_ao = AO.AO(Main(worker_ao))
        main_ao.start()
        self.aos_to_stop.append(main_ao)

        f = main_ao.use_bad(10)
        self.assertRaises(Exception,f.get)
        self.assertEquals(f.is_error(),True)
        self.assertEquals(str(f.get_error()),"BAD 2")                

    def test_badly_formed_coroutine(self):
        class Bad(PassiveObject):
            @AO.async_coroutine
            def bad_yield(self): yield 3

            @AO.async_coroutine
            def not_generator1(self): return 3

            @AO.async_coroutine
            def not_generator2(self): return 3  # wrong no of arguments

            @AO.async_coroutine
            def no_return(self): pass

        ao = AO.AO(Bad())
        ao.start()
        self.aos_to_stop.append(ao)

        f = ao.bad_yield()
        self.assertRaises(AO.AOException,f.get,2000)

        f = ao.no_return()
        self.assertRaises(AO.AOException,f.get,2000)

        f = ao.not_generator1()
        self.assertRaises(AO.AOException,f.get,2000)

        f = ao.not_generator2()
        self.assertRaises(AO.AOException,f.get,2000)

    def test_progress_mapping(self):
        class A(PassiveObject):
            @AO.async_coroutine
            def foo(self,f1,f2): 
                yield f1.progress_caller(50)
                yield f2.progress_caller(40)
                yield AO.AsyncRV(3)

        ao = AO.AO(A())
        ao.start()
        self.aos_to_stop.append(ao)

        f1 = Future()
        f2 = Future()

        f = ao.foo(f1,f2)
        self.assertEqual(f.get_progress().percent,0)

        f1.set_progress(40)
        time.sleep(0.5)
        self.assertEqual(f.get_progress().percent,20)

        f1.set(None)
        time.sleep(0.5)
        self.assertEqual(f.get_progress().percent,50)

        f2.set_progress(50)
        time.sleep(0.05)
        self.assertEqual(f.get_progress().percent,70)

        f2.set(None)
        val = f.get()
        self.assertEqual(val,3)
        self.assertEqual(f.get_progress().percent,100)
        
    def test_child_progress(self):
        def verify_progress(f, progress):
            yield f
            self.assertEqual(f.get_progress().percent, progress)
            
        class X(PassiveObject):
            @AO.async_coroutine
            def foo(self):
                verify_progress(y.foo1().progress_caller(30), 30)
                verify_progress(y.foo2().progress_caller_to(80), 80)
                verify_progress(AO.AO.progress_caller(20), 99)
                yield AO.AsyncRV(4)
            @AO.async_coroutine
            def foo_not_100_percent(self):
                verify_progress(y.foo1().progress_caller(30), 30)
                verify_progress(y.foo2().progress_caller_to(70), 70)
                verify_progress(AO.AO.progress_caller(10), 80)
                yield AO.AsyncRV(4)
        class Y(PassiveObject):
            @AO.async_coroutine
            def foo1(self):
                verify_progress(z.foobar().set_name("Z.foobar (from foo1)").progress_caller(50), 50)
                verify_progress(z.foobar().set_name("Z.foobar2nd (from foo1)").progress_caller(50), 99)
                yield AO.AsyncRV(None)
            @AO.async_coroutine
            def foo2(self):
                verify_progress(z.foobar().set_name("Z.foobar (from foo2)").progress_caller(50), 50)
                verify_progress(z.foobar().set_name("Z.foobar2nd (from foo2)").progress_caller(50), 99)
                yield AO.AsyncRV(None)
        class Z(PassiveObject):
            @AO.async_coroutine
            def foobar(self):
                yield AO.AsyncRV(None)
                
        y = AO.AO(Y())
        y.start()
        x = AO.AO(X())
        x.start()
        z = AO.AO(Z())
        z.start()
        
        lst_alert_msgs = []
        def alert_keeper(logger, msg_type, msg, **kw): #@UnusedVariable
            lst_alert_msgs.append(msg)

        original_alert_sender = assertions.Assertions.alert_sender
        assertions.Assertions.alert_sender = alert_keeper
        try:
            f = x.foo()
            if False: f=Future()
            res = f.get()
            self.assertEqual(f.get_progress().percent, 100)
            self.assertEqual(res, 4)
            self.assertEqual(len(lst_alert_msgs), 0)
            
            
            # test warning when not 100%
            f = x.foo_not_100_percent()
            res = f.get()
            self.assertEqual(f.get_progress().percent, 100)
            self.assertEqual(res, 4)
#            self.assertEqual(len(lst_alert_msgs), 1)
#            self.assertTrue("Progress of child coroutines accumulated to" in lst_alert_msgs[0])
        finally:
            z.quit()
            y.quit()
            x.quit()
            assertions.Assertions.alert_sender = original_alert_sender

    def test_sync_method(self):
        class A(PassiveObject):
            @AO.is_sync
            def sync(self): return id(threading.current_thread())
            def async(self): return self.sync()
        ao = AO.AO(A())
        ao.start()
        self.aos_to_stop.append(ao)

        main_thread = id(threading.current_thread())
        t1 = ao.sync()
        self.assertEqual(t1,main_thread)

        t2 = ao.async().get()
        self.assertNotEqual(t2,main_thread)

    def test_method_call_hooks(self):
        # create a method call hook that just tracks calls to itself
        from DTO import Bunch

        class CallHook(object):
            def __init__(self):
                self.events = []
                self.b_fail_commit = False
            def __call__(self,call_stage,call_type,cmd):
                d = util.dict_exclude(locals(),['self'])
                self.events.append(Bunch(**d))
                if call_stage == AO.MethodCallStage.Commit and self.b_fail_commit and not cmd.future.is_error():
                    raise TestException("failing commit")
                if call_stage == AO.MethodCallStage.Exit:
                    assertions.fail_unless(cmd.inner_future.is_set,"future is not set in method exit")
        hook = CallHook()

        # set up an active object with above method call hook
        class A(PassiveObject):
            @AO.is_sync
            def mth_sync(self,b_raise=False):
                if b_raise: raise TestException("xxx")
                return 666

            def mth_async(self,b_raise=False):
                if b_raise: raise TestException("xxx")
                return 666

            @AO.async_coroutine
            def mth_coroutine(self,f,b_raise=False):
                yield f
                if b_raise: raise TestException("xxx")
                yield AO.AsyncRV(666)

        ao = AO.AO(A())
        ao.method_call_hook = hook # install the hook
        ao.start()
        self.aos_to_stop.append(ao)

        # check sync method - good path
        hook.events = []
        hook.b_fail_commit = False
        ao.mth_sync()
        self.assertEqual([str(e.call_stage) for e in hook.events],['Request','Enter','Commit','Exit'])
        for e in hook.events:
            self.assertEqual(e.call_type,AO.MethodCallType.Sync)
            self.assertEqual(e.cmd.method_name,'mth_sync')
        cmd_future = hook.events[-1].cmd.future
        self.assertEqual(cmd_future.get(),666)

        # check sync method - bad path (method)
        hook.events = []
        hook.b_fail_commit = False
        self.assertRaises(TestException,ao.mth_sync,b_raise=True)
        self.assertEqual([str(e.call_stage) for e in hook.events],['Request','Enter','Commit','Exit'])
        for e in hook.events:
            self.assertEqual(e.call_type,AO.MethodCallType.Sync)
            self.assertEqual(e.cmd.method_name,'mth_sync')
        cmd_future = hook.events[-1].cmd.future
        self.assertEqual(str(cmd_future.get_error()),'xxx')

        # check sync method - bad path (commit)
        hook.events = []
        hook.b_fail_commit = True
        self.assertRaises(TestException,ao.mth_sync)
        self.assertEqual([str(e.call_stage) for e in hook.events],['Request','Enter','Commit','Exit'])
        for e in hook.events:
            self.assertEqual(e.call_type,AO.MethodCallType.Sync)
            self.assertEqual(e.cmd.method_name,'mth_sync')
        cmd_future = hook.events[-1].cmd.future
        self.assertEqual(str(cmd_future.get_error()),'failing commit')

        # check async method - good path
        hook.events = []
        hook.b_fail_commit = False
        ao.mth_async().get()
        time.sleep(0.1)
        self.assertEqual([str(e.call_stage) for e in hook.events],['Request','Enter','Commit','Exit'])
        for e in hook.events:
            self.assertEqual(e.call_type,AO.MethodCallType.Async)
            self.assertEqual(e.cmd.method_name,'mth_async')
        cmd_future = hook.events[-1].cmd.future
        self.assertEqual(cmd_future.get(),666)

        # check async method - bad path (method)
        hook.events = []
        hook.b_fail_commit = False
        self.assertRaises(TestException,ao.mth_async(b_raise=True).get)
        time.sleep(0.1)
        self.assertEqual([str(e.call_stage) for e in hook.events],['Request','Enter','Commit','Exit'])
        for e in hook.events:
            self.assertEqual(e.call_type,AO.MethodCallType.Async)
            self.assertEqual(e.cmd.method_name,'mth_async')
        cmd_future = hook.events[-1].cmd.future
        self.assertEqual(str(cmd_future.get_error()),'xxx')

        # check async method - bad path (commit)
        hook.events = []
        hook.b_fail_commit = True
        self.assertRaises(TestException,ao.mth_async().get)
        time.sleep(0.1)
        self.assertEqual([str(e.call_stage) for e in hook.events],['Request','Enter','Commit','Exit'])
        for e in hook.events:
            self.assertEqual(e.call_type,AO.MethodCallType.Async)
            self.assertEqual(e.cmd.method_name,'mth_async')
        cmd_future = hook.events[-1].cmd.future
        self.assertEqual(str(cmd_future.get_error()),'failing commit')

        # check coroutine - good path: enter + suspend
        hook.events = []
        hook.b_fail_commit = False
        f_control = Future()
        f = ao.mth_coroutine(f_control)
        time.sleep(0.1)
        self.assertEqual([str(e.call_stage) for e in hook.events],['Request','Enter','Suspend'])
        for e in hook.events:
            self.assertEqual(e.call_type,AO.MethodCallType.Coroutine)
            self.assertEqual(e.cmd.method_name,'mth_coroutine')
        cmd_future = hook.events[-1].cmd.future
        self.assertEqual(cmd_future.is_set(),False)

        # check coroutine - good path: resume + exit
        hook.events = []
        hook.b_fail_commit = False
        f_control.set(None) # allow coroutine to finish
        f.get() # wait for it to finish
        time.sleep(0.1)
        self.assertEqual([str(e.call_stage) for e in hook.events],['RequestResume','Resume','Commit','Exit'])
        for e in hook.events:
            self.assertEqual(e.call_type,AO.MethodCallType.Coroutine)
            self.assertEqual(e.cmd.method_name,'mth_coroutine')
        cmd_future = hook.events[-1].cmd.future
        self.assertEqual(cmd_future.get(),666)

        # check coroutine - bad path (method): enter + suspend
        hook.events = []
        hook.b_fail_commit = False
        f_control = Future()
        f = ao.mth_coroutine(f_control,b_raise=True)
        time.sleep(0.1)
        self.assertEqual([str(e.call_stage) for e in hook.events],['Request','Enter','Suspend'])
        for e in hook.events:
            self.assertEqual(e.call_type,AO.MethodCallType.Coroutine)
            self.assertEqual(e.cmd.method_name,'mth_coroutine')
        cmd_future = hook.events[-1].cmd.future
        self.assertEqual(cmd_future.is_set(),False)

        # check coroutine - bad path (method): resume + exit
        hook.events = []
        hook.b_fail_commit = False
        f_control.set(None) # allow coroutine to finish
        self.assertRaises(TestException,f.get) # wait for it to finish
        time.sleep(0.1)
        self.assertEqual([str(e.call_stage) for e in hook.events],['RequestResume','Resume','Commit','Exit'])
        for e in hook.events:
            self.assertEqual(e.call_type,AO.MethodCallType.Coroutine)
            self.assertEqual(e.cmd.method_name,'mth_coroutine')
        cmd_future = hook.events[-1].cmd.future
        self.assertEqual(str(cmd_future.get_error()),'xxx')

        # check coroutine - bad path (commit): enter + suspend
        hook.events = []
        hook.b_fail_commit = True
        f_control = Future()
        f = ao.mth_coroutine(f_control)
        time.sleep(0.1)
        self.assertEqual([str(e.call_stage) for e in hook.events],['Request','Enter','Suspend'])
        for e in hook.events:
            self.assertEqual(e.call_type,AO.MethodCallType.Coroutine)
            self.assertEqual(e.cmd.method_name,'mth_coroutine')
        cmd_future = hook.events[-1].cmd.future
        self.assertEqual(cmd_future.is_set(),False)

        # check coroutine - bad path (commit): resume + exit
        hook.events = []
        hook.b_fail_commit = True
        f_control.set(None) # allow coroutine to finish
        self.assertRaises(TestException,f.get) # wait for it to finish
        time.sleep(0.1)
        self.assertEqual([str(e.call_stage) for e in hook.events],['RequestResume','Resume','Commit','Exit'])
        for e in hook.events:
            self.assertEqual(e.call_type,AO.MethodCallType.Coroutine)
            self.assertEqual(e.cmd.method_name,'mth_coroutine')
        cmd_future = hook.events[-1].cmd.future
        self.assertEqual(str(cmd_future.get_error()),'failing commit')

    def test_sync_facade(self):
        class A(PassiveObject):
            def get_thread(self):
                return id(threading.current_thread())

            @AO.sync_facade
            def mth_async(self):
                return id(threading.current_thread())

            @AO.sync_facade
            @AO.async_coroutine
            def mth_coroutine(self):
                yield AO.AsyncRV(id(threading.current_thread()))
        ao = AO.AO(A())
        ao.start()
        self.aos_to_stop.append(ao)

        t_id = ao.get_thread().get()
        self.assertNotEqual(t_id, id(threading.current_thread()))

        t_id2 = ao.mth_async()
        self.assertEqual(t_id2,t_id)

        t_id3 = ao.mth_coroutine()
        self.assertEqual(t_id3,t_id2)

    def test_wrappers(self):
        def multi_call(n_times):
            def wrapper(self,wrapped,*a,**kw):
                all_res = []
                for _ in xrange(n_times):
                    res = yield wrapped(*a,**kw)
                    all_res.append(res)
                yield AO.AsyncRV(all_res)
            return wrapper                

        def wrap_it(self,wrapped,x,y):
            total = yield wrapped(x,y)
            total += self.i
            yield AO.AsyncRV(total)

        class A(PassiveObject):
            def __init__(self,i):
                super(A,self).__init__()
                self.i = i

            @AO.wrap_with(multi_call(2))
            @AO.wrap_with(wrap_it)
            def add(self,x,y): 
                return x+y

            @AO.wrap_with(multi_call(3))
            @AO.wrap_with(wrap_it)
            @AO.async_coroutine
            def coroutine_add(self,x,y): 
                yield AO.AsyncRV(x+y)

        ao = AO.AO(A(10))
        ao.start()
        self.aos_to_stop.append(ao)

        # check wrapping of normal async method
        total = ao.add(2,3).get()
        self.assertEqual(total,[15,15])

        # check wrapping of coroutine
        total = ao.coroutine_add(2,3).get()
        self.assertEqual(total,[15,15,15])

    def test_wrapper_names(self):
        def wrap_it(self,wrapped):
            yield AO.AsyncRV( (wrapped.__name__,wrapped.base_name) )

        class A(PassiveObject):
            @AO.wrap_with(wrap_it)
            def foo(self): pass

            @AO.wrap_with(wrap_it)
            @AO.wrap_with(wrap_it)
            @AO.wrap_with(wrap_it)
            def bar(self): pass

        ao = AO.AO(A())
        ao.start()
        self.aos_to_stop.append(ao)

        name = ao.foo().get()
        self.assertEqual(name,('foo','foo'))

        name = ao.bar().get()
        self.assertEqual(name,('wrap_it(wrap_it(bar))','bar'))
        
    def test_method_call_hooks_with_wrapped(self):
        # create a method call hook that just tracks calls to itself
        class CallHook(object):
            def __init__(self):
                self.reset()
                self.called_with_wrapped_wrapper = False

            def reset(self):
                self.lst_calls = []

            def __call__(self,
                         call_stage,
                         call_type, #@UnusedVariable
                         cmd): 
                if call_stage == AO.MethodCallStage.Enter: # only 'log' one stage per call
                    self.lst_calls.append(cmd.method_name)
                if hasattr(cmd.method,'is_wrapped'):
                    self.called_with_wrapped_wrapper = True
                    
        hook = CallHook()
        
        def wrap_wrapper(f):
            f.is_wrapped = True
            return f
        @wrap_wrapper
        def wrap_it(self,wrapped,*a,**kw):
            yield wrapped(*a,**kw)
            yield AO.AsyncRV(None)

        # set up an active object with above method call hook
        class A(PassiveObject):
            def foo(self):
                return 'foo'

            @AO.wrap_with(wrap_it)
            @AO.wrap_with(wrap_it)
            def wrapped_foo(self):
                return 'wrapped_foo'

        ao = AO.AO(A())
        ao.method_call_hook = hook # install the hook
        ao.start()
        self.aos_to_stop.append(ao)

        # check non wrapped method
        ao.foo().get()
        self.assertEqual(hook.lst_calls,['foo'])
        self.assertEqual(hook.called_with_wrapped_wrapper, False)

        # check wrapped method
        hook.reset()
        ao.wrapped_foo().get()
        self.assertEqual(hook.lst_calls,['wrap_it(wrap_it(wrapped_foo))','wrap_it(wrapped_foo)','wrapped_foo'])
        self.assertEqual(hook.called_with_wrapped_wrapper, True)

    def test_invoke_wrapped(self):
        def multi_call(n_times):
            def wrapper(self,wrapped,*a,**kw):
                all_res = []
                for _ in xrange(n_times):
                    res = yield wrapped(*a,**kw)
                    all_res.append(res)
                yield AO.AsyncRV(all_res)
            return wrapper                

        class A(PassiveObject):
            def __init__(self,i):
                super(A,self).__init__()
                self.i = i

            @AO.async_coroutine                
            def foo(self,x,y):
                # define inner function and wrap it
                @AO.wrap_with(multi_call(2))
                @AO.async_coroutine
                def add(a,b):
                    yield AO.AsyncRV(self.i + a + b)
                res = yield self._ao.AO_invoke(add,x,y)
                yield AO.AsyncRV(res)

        ao = AO.AO(A(10))
        ao.start()
        self.aos_to_stop.append(ao)

        # check wrapping of normal async method
        total = ao.foo(2,3).get()
        self.assertEqual(total,[15,15])

    def test_cancel_task(self):
        class AOHook(object):
            def __init__(self):
                self.method_to_fail_at_enter = None            
                self.method_to_fail_at_resume = None
            def __call__(self,
                         call_stage,
                         call_type, #@UnusedVariable
                         cmd):
                if cmd.method_name == self.method_to_fail_at_enter and call_stage == AO.MethodCallStage.Request:
                    return Future.preset_error(TestException('cancelled at enter'))
                if cmd.method_name == self.method_to_fail_at_resume and call_stage == AO.MethodCallStage.RequestResume:
                    return Future.preset_error(TestException('cancelled at resume'))

        ao_hook = AOHook()

        # set up an active object with above method call hook
        class A(PassiveObject):
            def __init__(self):
                super(A,self).__init__()
                self.reset()

            def reset(self):
                self.lst = []
                self.f_continue1 = Future()
                self.f_continue2 = Future()
                self.f_checkpoint1 = Future()
                self.f_checkpoint2 = Future()

            @AO.async_coroutine
            def foo(self):
                self.lst.append(1)
                self.f_checkpoint1.set(None)
                try:
                    yield self.f_continue1
                except TestException:
                    self.f_checkpoint2.set(None)                                        
                    raise
                self.lst.append(2)
                yield AO.AsyncRV(None)

        a = A()
        ao = AO.AO(a)
        ao.method_call_hook = ao_hook # install the hook
        ao.start()
        self.aos_to_stop.append(ao)

        # check cancellation at Enter stage
        ao_hook.method_to_fail_at_enter = 'foo'

        # verifying cancel in ao (Enter stage)
        f = ao.foo()
        self.assertRaises(TestException,f.get,1000)
        self.assertEqual(str(f.get_error()),'cancelled at enter')  
        self.assertEqual(a.lst,[])  
        a.reset()

        # check cancellation at Resume stage
        ao_hook.method_to_fail_at_enter = None  
        ao_hook.method_to_fail_at_resume = 'foo'

        # verifying cancel in ao (Resume stage)
        f = ao.foo()
        a.f_checkpoint1.get(1000)
        self.assertEqual(a.f_checkpoint2.is_set(),False)
        a.f_continue1.set(None)
        self.assertEqual(a.f_checkpoint2.get(),None)# verifying TaskException raised
        self.assertRaises(TestException,f.get,1000)
        self.assertEqual(str(f.get_error()),'cancelled at resume')
        self.assertEqual(a.lst,[1])
        a.reset()
        
    def test_dynamic_proxy_object(self):
        class A(DynamicProxy):
            def __init__(self):                
                DynamicProxy.__init__(self)
                self.logger = get_logger('A')
                
            def _dispatch(self,
                          method_name,
                          *a, #@UnusedVariable
                          **kw): #@UnusedVariable
                return method_name
        ao = AO.AO(A())
        ao.start()
        self.aos_to_stop.append(ao)
        
        f = ao.foo()
        x = f.get(500)
        self.assertEqual(x,'foo')
        self.assertEqual(f.name,'A.foo')

class TestFlowChangingHooks(TestAOCommonSetup):
    class CallHook(object):
        def __init__(self,stage,retval=None,exc=None,b_manual_finish=False):
            self.stage = stage
            self.f = Future()
            self.f_continue = Future()
            if not b_manual_finish:
                self.f_continue.set(None)
                
            def set_future(f_continue,**kw): #@UnusedVariable
                if exc is None:
                    if retval is not None:
                        self.f.set(AO.AsyncRV(retval))
                    else:
                        self.f.set(None)
                else:
                    self.f.set_error(exc)
            self.f_continue.attach_observer(set_future)
            
        def allow_finish(self):
            self.f_continue.set(None)
            
        def __call__(self,
                     call_stage,
                     call_type, #@UnusedVariable
                     cmd): #@UnusedVariable
            if call_stage != self.stage:
                return None
            return self.f

    class A(PassiveObject):
        def __init__(self):
            super(TestFlowChangingHooks.A,self).__init__()
            self.stage = 0
            
        @AO.is_sync
        def mth_sync(self):
            self.stage = 1
            return 666
        
        def mth_async(self):
            self.stage = 1
            return 666
        
        @AO.async_coroutine
        def mth_coroutine(self):
            self.stage = 0.5
            x = yield Future.preset(None)
            self.stage = 1
            if x is not None:
                yield AO.AsyncRV(2*x)
            else:
                yield AO.AsyncRV(666)
        
    def setUp(self):
        super(TestFlowChangingHooks,self).setUp()
        self.CallHook = TestFlowChangingHooks.CallHook

        self.ao = AO.AO(TestFlowChangingHooks.A())
        self.ao.start()
        self.aos_to_stop.append(self.ao)
        
        class Sat(PassiveObject):
            def ping(self):
                pass
        self.sat = AO.SatelliteAO(Sat(),self.ao)
        
    def _test_enter_exit(self,method_stage):
        assertions.fail_unless(method_stage in [AO.MethodCallStage.Request, AO.MethodCallStage.Exit], "Unexpected method_stage", method_stage=method_stage)
        if method_stage == AO.MethodCallStage.Request:
            expected_stage = 0
        else:
            expected_stage = 1
        
        # change return value
        self.ao.obj.stage = 0
        self.ao.method_call_hook = self.CallHook(method_stage, retval=111)
        retval = self.ao.mth_async().get(1000)
        self.assertEqual(retval,111)
        self.assertEqual(self.ao.obj.stage,expected_stage)

        # manual finish
        self.ao.obj.stage = 0
        self.ao.method_call_hook = self.CallHook(method_stage, b_manual_finish=True)
        f = self.ao.mth_async()
        self.assertRaises(FutureTimeoutException, f.get, 500)
        self.assertEqual(self.ao.obj.stage,expected_stage)
        self.assertRaises(FutureTimeoutException,self.sat.ping().get,500) # verify thread is blocked for normal async method
        self.ao.method_call_hook.allow_finish()
        retval = f.get(500)
        self.assertEqual(retval,666)

        # throw exception
        self.ao.obj.stage = 0
        self.ao.method_call_hook = self.CallHook(method_stage, exc=TestException())
        f = self.ao.mth_async()
        self.assertRaises(TestException, f.get, 500)
        self.assertEqual(self.ao.obj.stage,expected_stage)
        
        # coroutine - change return value (with manual finish hook)
        self.ao.obj.stage = 0
        self.ao.method_call_hook = self.CallHook(method_stage, retval=111, b_manual_finish=True)
        f = self.ao.mth_coroutine()
        self.assertRaises(FutureTimeoutException, f.get, 500)
        self.assertEqual(self.ao.obj.stage,expected_stage)
        self.sat.ping().get(500) # verify thread is not blocked for coroutine while we wait
        self.ao.method_call_hook.allow_finish()
        retval = f.get(500)
        self.assertEqual(retval,111)

        # sync method - change return value
        self.ao.obj.stage = 0
        self.ao.method_call_hook = self.CallHook(method_stage, retval=111)
        retval = self.ao.mth_sync()
        self.assertEqual(retval,111)
        self.assertEqual(self.ao.obj.stage,expected_stage)
        
    def test_enter(self):
        self._test_enter_exit(AO.MethodCallStage.Request)

    def test_exit(self):
        self._test_enter_exit(AO.MethodCallStage.Exit)

    def test_resume(self):
        # throw exception
        self.ao.obj.stage = 0
        self.ao.method_call_hook = self.CallHook(AO.MethodCallStage.RequestResume, exc=TestException())
        f = self.ao.mth_coroutine()
        self.assertRaises(TestException, f.get, 500)
        self.assertEqual(self.ao.obj.stage,0.5)

        # change return value (with manual finish hook)
        self.ao.obj.stage = 0
        self.ao.method_call_hook = self.CallHook(AO.MethodCallStage.RequestResume, retval=111, b_manual_finish=True)
        f = self.ao.mth_coroutine()
        self.assertRaises(FutureTimeoutException, f.get, 500)
        self.assertEqual(self.ao.obj.stage,0.5)
        self.sat.ping().get(500) # verify thread is not blocked for coroutine while we wait
        self.ao.method_call_hook.allow_finish()
        retval = f.get(500)
        self.assertEqual(retval,222)        
        self.assertEqual(self.ao.obj.stage,1)
                
class TestSyncFacade(TestAOCommonSetup):
    def test_sanity(self):
        class A(PassiveObject):
            def add(self,x,y): return x+y
        ao = AO.AO(A())
        ao.start()
        self.aos_to_stop.append(ao)        
        sync = AO.SyncFacade(ao)
        total = sync.add(2,3)
        self.assertEqual(total,5)

    def test_tostring(self):
        class A(PassiveObject):
            pass
        ao = AO.AO(A())
        sync = AO.SyncFacade(ao)
        self.assertEqual(str(sync),'SyncFacade(AO(A))')
        
    def test_dir(self):
        class A(PassiveObject):
            def foo(self): pass
        ao = AO.AO(A())
        sync = AO.SyncFacade(ao)
        d = dir(sync)
        self.assert_('foo' in d)
        self.assertEqual(d,dir(ao))

    def test_sync_method(self):
        class A(PassiveObject):
            @AO.is_sync
            def add(self,x,y): return x+y
        ao = AO.AO(A())
        ao.start()
        self.aos_to_stop.append(ao)
        sync = AO.SyncFacade(ao)
        total = sync.add(2,3)
        self.assertEqual(total,5)

from unit import build_suite, run_suite, combine_suites
def suite():
    return combine_suites(
        build_suite(TestAO), 
        build_suite(TestFlowChangingHooks),
        build_suite(TestSyncFacade),
    )

if __name__ == '__main__':
    run_suite(suite())
