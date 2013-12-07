from test_infra_base import BackendInfraTest
import future
from util import curry
import threading
import assertions
from stopwatch import Stopwatch
from mock.timer import TimerManager as MockTimerManager
from future import ProgressObserver

import exceptions
class TestException(exceptions.Exception):
    pass

class Result(object):
    def __init__(self):
        self.val = None

class TestFuture(BackendInfraTest):    
    def setUp(self):
        super(TestFuture,self).setUp()
        assertions.Assertions.reset_events()
        self.result = Result()

    def tearDown(self):
        self.failIf(assertions.Assertions.had_assertion)

    def test_normal(self):
        f = future.Future()
        self.failIf(f.is_set())

        threading.Thread(target=curry(f.set, 3)).run()
        val = f.get()
        self.failUnless(f.is_set())
        self.assertEqual(val,3)
        
    def test_wait(self):
        f = future.Future()
        self.failIf(f.is_set())
        threading.Thread(target=curry(f.set, 3)).run()
        f.wait()
        self.failUnless(f.is_set())
        self.assertEqual(f.get(),3)

        f = future.Future()
        self.failIf(f.is_set())
        threading.Thread(target=curry(f.set_error, Exception())).run()
        f.wait()
        self.failUnless(f.is_set())
        self.assertEqual(f.is_error(),True)
        
    def test_get_val_or_error(self):
        f = future.Future()
        self.assertRaises(assertions.AssertionException,f.get_val_or_error)
        assertions.Assertions.had_assertion = False # silence the check at end of test
        
        f.set(3)
        val,exc = f.get_val_or_error()
        self.assertEqual(val,3)
        self.assertEqual(exc,None)
        
        f = future.Future()
        my_exc = TestException('bla')
        f.set_error(my_exc)
        val,exc = f.get_val_or_error()
        self.assertEqual(val,None)
        self.assertEqual(exc,my_exc)
        
    def test_unicode_value(self):
        def test_f(s, b_unicode=True):
            f = future.Future()
            f.set_name("test_name")
            f.set(s)
            print f
            s = "Future(Name:test_name %s)" %(s,)
            expected = s.encode('raw_unicode_escape') if b_unicode else s
            self.assertEqual(f.__str__(), expected)
        
        test_f(u'\u0592\u0589\u0583\u0585')
        test_f('bla bla')
        test_f(u"\xaa", True)
        test_f("\xaa", False)
        

    def test_set_val_or_error(self):
        f = future.Future()
        self.assertRaises(assertions.AssertionException,f.get_val_or_error)
        assertions.Assertions.had_assertion = False # silence the check at end of test
        
        f.set_val_or_error(val=3)
        val,exc = f.get_val_or_error()
        self.assertEqual(val,3)
        self.assertEqual(exc,None)
        
        f = future.Future()
        my_exc = TestException('bla')
        f.set_val_or_error(exc=my_exc)
        val,exc = f.get_val_or_error()
        self.assertEqual(val,None)
        self.assertEqual(exc,my_exc)
        
    def test_str(self):
        f = future.Future().set_name('name')
        self.assertEqual(str(f),"Future(Name:name 0% ready)")
        f.set_progress(50)
        self.assertEqual(str(f),"Future(Name:name 50% ready)")
        f.set(4)
        self.assertEqual(str(f),"Future(Name:name 4)")
        f = future.Future.preset_error(Exception("problem")).set_name('name')
        self.assertEqual(str(f),"Future(Name:name Error)")

    def test_name(self):
        f = future.Future()
        self.assertEqual(f.name,None)
        f2 = f.set_name('bla')
        self.assertEqual(f2,f)
        self.assertEqual(f.name,'bla')
        
    def test_set_none(self):
        f = future.Future()
        f.set(None)
        val = f.get()
        self.failUnless(f.is_set())
        self.assertEqual(val,None)

    def test_preset(self):
        f = future.Future.preset('james')
        self.failUnless(f.is_set())
        val = f.get()
        self.assertEqual(val,'james')

    def test_preset_error(self):
        f = future.Future.preset_error(TestException('BAD'))
        self.failUnless(f.is_set())
        self.failUnless(f.is_error())
        self.assertEqual(str(f.get_error()),'BAD')

    def test_observers(self):
        f = future.Future()

        def observer(the_future, **kw):
            self.assert_(the_future.is_set())
            self.assertEqual(self.result.val,None)
            self.result.val = (the_future.get(), id(threading.current_thread()))

        f.attach_observer(observer)
        f.set_progress(50) # verify observer not called (it would assert)
        t = threading.Thread(target=curry(f.set, 'a name'))            
        t.start()
        t.join()
        self.failUnless(f.is_set())
        self.assertEqual(self.result.val, ('a name', id(t)))

        self.result.val = None
        f.attach_observer(observer) # attaching observer after future is set calls observer immediately (from our thread)
        self.assertEqual(self.result.val, ('a name', id(threading.current_thread())))

    def test_set_error(self):
        f = future.Future()
        threading.Thread(target=curry(f.set_error, TestException('BAD'))).run()
        self.assertRaises(TestException,f.get)
        self.failUnless(f.is_set())
        self.failUnless(f.is_error())
        self.assertEqual(str(f.get_error()),'BAD')

    def test_track_future(self):
        def reset():
            f = future.Future()
            f2 = future.Future()
            f2.track_future(f)
            return f, f2
        f, f2 = reset()
        f.set(10)
        self.assertEqual(f2.get(), 10)
        f, f2 = reset()
        f.set_progress(50)
        self.assertEqual(f2.get_progress().percent, 50)
        f, f2 = reset()
        f.set_error(Exception('Oh my GOD'))
        self.assertEqual(f2.is_error(), True)
        
    def test_progress(self):
        f = future.Future()
        progress = f.get_progress()        
        self.assertEqual(progress.percent,0)
        self.assertEqual(progress.is_set,False)
        self.assertEqual(progress.is_error,False)
        self.assertEqual(progress.error,None)
        fv = f.get_frozen_value()
        self.assertEqual(fv.progress,progress)
        self.assertEqual(fv.value,None)

        f.set_progress(50)
        progress = f.get_progress()
        self.assertEqual(progress.percent,50)
        self.assertEqual(progress.is_set,False)
        self.assertEqual(progress.is_error,False)
        self.assertEqual(progress.error,None)
        fv = f.get_frozen_value()
        self.assertEqual(fv.progress,progress)
        self.assertEqual(fv.value,None)

        f.set_progress(33)
        progress = f.get_progress()
        self.assertEqual(progress.percent,50)

        f.set_progress(33,b_allow_regression=True)
        progress = f.get_progress()
        self.assertEqual(progress.percent,33)

        f.set(3)
        progress = f.get_progress()
        self.assertEqual(progress.percent,100)
        self.assertEqual(progress.is_set,True)
        self.assertEqual(progress.is_error,False)
        self.assertEqual(progress.error,None)
        fv = f.get_frozen_value()
        self.assertEqual(fv.progress,progress)
        self.assertEqual(fv.value,3)

        f = future.Future()
        f.set_progress(50)
        exc = Exception('xxx')
        f.set_error(exc)
        progress = f.get_progress()
        self.assertEqual(progress.percent,0)
        self.assertEqual(progress.is_set,True)
        self.assertEqual(progress.is_error,True)        
        self.assertEqual(progress.error,exc)
        fv = f.get_frozen_value()
        self.assertEqual(fv.progress,progress)
        self.assertEqual(fv.value,None)

    def test_progress_observer(self):
        f = future.Future()
        main_thread_id = id(threading.current_thread())

        result_many = Result()        
        def observe_many(the_future, **kw):
            result_many.val = (the_future.get_progress().percent, id(threading.current_thread()))

        result_once = Result()        
        def observe_once(the_future, **kw):
            self.assertEqual(result_once.val,None)
            result_once.val = (the_future.get_progress().percent, id(threading.current_thread()))

        f.attach_observer(observe_many, b_notify_on_progress=True)
        f.attach_observer(observe_once, b_notify_on_progress=True,b_notify_once=True)
        t = threading.Thread(target=curry(f.set_progress, 50))
        t.start()
        t.join()
        self.assertEqual(f.get_progress().percent, 50)
        self.assertEqual(result_many.val, (50, id(t)))
        self.assertEqual(result_once.val, (50, id(t)))

        result_immediate = Result()
        def observe_immediate(the_future, **kw):
            result_immediate.val = (the_future.get_progress().percent, id(threading.current_thread()))
        f.attach_observer(observe_immediate,b_notify_on_progress=True)
        self.assertEqual(result_immediate.val,(50,main_thread_id))

        result_not_immediate = Result()
        def observe_not_immediate(the_future, **kw):
            result_not_immediate.val = (the_future.get_progress().percent, id(threading.current_thread()))
        f.attach_observer(observe_not_immediate,b_notify_on_progress=True,b_notify_immediate_progress=False)
        self.assertEqual(result_not_immediate.val,None)
        
        t2 = threading.Thread(target=curry(f.set_progress, 75))
        t2.start()
        t2.join()
        self.assertEqual(f.get_progress().percent,75)
        self.assertEqual(result_many.val, (75, id(t2)))
        self.assertEqual(result_once.val, (50, id(t)))
        self.assertEqual(result_immediate.val,(75, id(t2)))
        self.assertEqual(result_not_immediate.val,(75, id(t2)))

    def test_progress_chaining(self):
        f1 = future.Future()
        f2 = future.Future()
        f3 = future.Future()

        f2.chain_progress(f1)
        f3.chain_progress(f1,progress_mapping=(20,30))

        f1.set_progress(10)
        self.assertEqual(f2.get_progress().percent,10)
        self.assertEqual(f3.get_progress().percent,21)

        f1.set(None)
        self.assertEqual(f2.get_progress().percent,99)
        self.assertEqual(f3.get_progress().percent,30)

    def test_progress_max_value(self):
        f = future.Future()
        progress = f.get_progress()        
        self.assertEqual(progress.percent,0)
        self.assertEqual(progress.is_set,False)
        self.assertEqual(progress.is_error,False)

        f.set_progress(100)
        progress = f.get_progress()
        self.assertEqual(progress.percent,99)
        self.assertEqual(progress.is_set,False)
        self.assertEqual(progress.is_error,False)

        f.set(3)
        progress = f.get_progress()
        self.assertEqual(progress.percent,100)
        self.assertEqual(progress.is_set,True)
        self.assertEqual(progress.is_error,False)

    def test_timeout(self):
        # preset future - should return within timeout
        f = future.Future.preset(3)
        self.assertEqual(f.get(100),3)

        # unset future - should raise exception
        timeout = 1 # timeout in seconds
        f = future.Future()
        stopwatch = Stopwatch()
        stopwatch.start()
        self.assertRaises(future.FutureTimeoutException,f.get,timeout*1000)
        duration = stopwatch.duration()
        self.assert_(0.9*timeout < duration < 1.3*timeout, 'duration=%s' % duration)  

    def test_set_by_other_future(self):
        f1 = future.Future()              
        f2 = future.Future()
        threading.Thread(target=curry(f1.set, 3)).run()
        f1.get()
        self.failUnless(f1.is_set())
        f2.set_by_other_future_value(f1)
        self.failUnless(f2.is_set())
        self.assertEqual(f2.get(),3)        

        #set error:
        f1 = future.Future()
        f2 = future.Future()
        threading.Thread(target=curry(f1.set_error,TestException('BAD'))).run()
        self.assertRaises(TestException,f1.get)
        f2.set_by_other_future_value(f1)
        self.assertRaises(TestException,f2.get)
        self.assertEqual(str(f2.get_error()),'BAD')

    def test_add_timeout(self):
        self.timer_manager = MockTimerManager(factory=None)       
        
        def verify_num_timers(n):
            st_timers = self.timer_manager.TEST_get_all_timers()
            self.assertEqual(len(st_timers),n)
        
        # verify timeout works
        timeout = 200
        f = future.Future()
        f.add_timeout(self.timer_manager,timeout) 
        verify_num_timers(1)
        self.assert_(not f.is_set())
        self.timer_manager.advance_time(timeout)
        self.assertRaises(future.FutureTimeoutException, f.get)
        self.assert_(f.is_set())
        self.assert_(f.is_error()) 
        verify_num_timers(0) # verify timer cancelled

        # verify set before timeout
        f = future.Future()
        f.add_timeout(self.timer_manager,timeout) 
        verify_num_timers(1)
        self.timer_manager.advance_time(timeout/2)
        self.assert_(not f.is_set())        
        f.set(33)
        verify_num_timers(0) # all timeout timers on a future should be canceled when it is set
        x = f.get()
        self.assertEqual(x,33)
        
    def test_start_auto_progress(self):
        timer_manager = MockTimerManager(factory=None)
        f = future.Future()
        self.assertEqual(f.get_progress().percent,0)
        f.start_auto_progress(timer_manager,1000,100)
        timer_manager.advance_time(250)
        self.assertEqual(f.get_progress().percent,30)
        timer_manager.advance_time(300)
        self.assertEqual(f.get_progress().percent,60)
        timer_manager.advance_time(500)
        self.assertEqual(f.get_progress().percent,99)
        timer_manager.advance_time(1000)
        self.assertEqual(f.get_progress().percent,99)
        st_timers = timer_manager.TEST_get_all_timers()
        self.assertEqual(len(st_timers),1)
        f.set(33)
        self.assertEqual(len(st_timers),0) # all auto_progress timers on a future should be canceled when it is set
        
class TestFutureAggregator(BackendInfraTest):
    def setUp(self):
        super(TestFutureAggregator,self).setUp()
        self.result = Result()

    def test_sanity(self):
        f1 = future.Future()
        f2 = future.Future()
        agg = future.FutureAggregator()
        self.assertEqual(agg.get_size(),0)
        agg.add_future(f1)
        self.assertEqual(agg.get_size(),1)
        agg.add_future(f2)
        self.assertEqual(agg.get_size(),2)
        agg_f = agg.activate()
        self.assertEqual(agg.get_size(),2)

        self.failIf(agg_f.is_set())
        f1.set(3)
        self.failIf(agg_f.is_set())
        self.assertEqual(agg.get_size(),2)
        f2.set(4)
        self.failUnless(agg_f.is_set())
        agg_val = agg_f.get()
        self.assertEqual(agg.get_size(),2)
        self.assertEqual(agg_val,[3,4])

    def _test(self, b_immediate, b_set_error):
        agg = future.FutureAggregator()

        exc_string = 'EXC_STRING'        
        n_total = 10
        if b_immediate:
            n_unset = 0 
        else:
            n_unset = 5

        unset_futures = [future.Future() for i in range(n_unset)]
        for f in unset_futures:
            agg.add_future(f)

        # add some more futures that are already set
        for i in range(n_unset,n_total):
            f = future.Future()
            if b_set_error and b_immediate and (i%2==0):
                f.set_error(TestException(exc_string))
            else:
                f.set(i)
            agg.add_future(f)

        agg_f = agg.activate()

        def observer(the_future, **kw):
            self.failUnless(the_future.is_set())
            thread_id = id(threading.current_thread())
            if not b_set_error:
                res = sum(the_future.get())
            else:
                self.failUnless(the_future.is_error())
                res = the_future.get_error()
            self.result.val = (res,thread_id)
        agg_f.attach_observer(observer)

        threads = []
        for i,f in enumerate(unset_futures):
            if b_set_error and (i%2 == 0):
                target = curry(f.set_error,TestException(exc_string))
            else:
                target = curry(f.set,i)
            t = threading.Thread(target=target)
            threads.append(t)
            t.start()

        for t in threads: # wait for all threads. this also guarantees that self.result.val will already have been set
            t.join()
        res,tid = self.result.val
        if b_set_error:
            self.assertEqual(str(res),exc_string)
        else:
            self.assertEqual(res,sum(range(n_total)))
        main_thread_id = id(threading.current_thread())
        if b_immediate:
            self.failUnless(tid == main_thread_id)
        else:
            self.failIf(tid == main_thread_id)
            self.failUnless(tid in [id(t) for t in threads])

    def test_normal(self): self._test(False,False)
    def test_all_preset(self): self._test(True,False)
    def test_error(self): self._test(False,True)
    def test_preset_error(self): self._test(True,True)

    def test_zero_futures(self):
        agg = future.FutureAggregator()
        f = agg.activate()
        self.assertEqual(f.is_set(),True)
        val = f.get()
        self.assertEqual(val,[])

    def test_value_aggregator(self):
        f1 = future.Future()
        f2 = future.Future()
        agg = future.FutureAggregator(sum)
        agg.add_future(f1)
        agg.add_future(f2)
        agg_f = agg.activate()
        f1.set(3)
        f2.set(4)
        self.failUnless(agg_f.is_set())
        agg_val = agg_f.get()
        self.assertEqual(agg_val,7)

    def test_progress(self):
        f1 = future.Future()
        f2 = future.Future()
        agg = future.FutureAggregator()
        agg.add_future(f1)
        agg.add_future(f2)
        agg_f = agg.activate()

        self.assertEqual(agg_f.get_progress().percent,0)

        f1.set_progress(50)
        self.assertEqual(agg_f.get_progress().percent,25)

        f1.set(3)
        self.assertEqual(agg_f.get_progress().percent,50)

        f2.set(10)
        self.assertEqual(agg_f.get_progress().percent,100)

    def test_progress_error(self):
        f1 = future.Future()
        f2 = future.Future()
        agg = future.FutureAggregator()
        agg.add_future(f1)
        agg.add_future(f2)
        agg_f = agg.activate()

        self.assertEqual(agg_f.get_progress().percent,0)

        f1.set_progress(50)
        self.assertEqual(agg_f.get_progress().percent,25)

        f2.set_progress(50)
        self.assertEqual(agg_f.get_progress().percent,50)

        f1.set_error(Exception('xxx'))
        self.assertEqual(agg_f.get_progress().percent,50) # f1 progress becomes 0, but aggregate future not allowed to regress

        f2.set(34)
        self.assertEqual(agg_f.get_progress().percent,0) # once future is ready and has error, progress drops to 0


class TestFutureAny(BackendInfraTest):
    def setUp(self):
        super(TestFutureAny,self).setUp()
        self.result = Result()

    def test_sanity(self):
        def check(b_use_first,b_error):
            f1 = future.Future()
            f2 = future.Future()
            f_any = future.FutureAny(f1,f2).activate()
            self.failIf(f_any.is_set())

            f = f1 if b_use_first else f2
            if b_error:
                f.set_error(Exception('bla'))
            else:
                f.set(3)
            self.failUnless(f_any.is_set())
            self.assertEqual(f_any.is_error(),b_error)
            if b_error:
                self.assertEqual(str(f_any.get_error()),'bla')
            else:
                self.assertEqual(f_any.get(),3)

        check(True,True)
        check(True,False)
        check(False,True)
        check(False,False)
        
    def test_preset(self):
        f1 = future.Future.preset(3)
        f2 = future.Future()
        f_any = future.FutureAny(f1,f2).activate()
        self.failUnless(f_any.is_set())
        self.assertEqual(f_any.get(),3)

        f1 = future.Future.preset_error(Exception('bla'))
        f_any = future.FutureAny(f1).activate()
        self.failUnless(f_any.is_set())
        self.assertEqual(str(f_any.get_error()),'bla')
        
    def test_zero_futures(self):
        f_any = future.FutureAny()
        self.assertRaises(assertions.AssertionException,f_any.activate)

    def test_progress(self):
        f1 = future.Future()
        f2 = future.Future()
        f_any = future.FutureAny(f1,f2).activate()
        self.assertEqual(f_any.get_progress().percent,0)

        f1.set_progress(50)
        self.assertEqual(f_any.get_progress().percent,50)
        f2.set_progress(30)
        self.assertEqual(f_any.get_progress().percent,50)
        f2.set_progress(70)
        self.assertEqual(f_any.get_progress().percent,70)
        
        f1.set(3)
        self.assertEqual(f_any.get_progress().percent,f1.get_progress().percent)

        # now same thing, but finish with error
        f1 = future.Future()
        f2 = future.Future()
        f_any = future.FutureAny(f1,f2).activate()
        f1.set_progress(50)
        self.assertEqual(f_any.get_progress().percent,50)
        f2.set_error(Exception('bla'))
        self.assertEqual(f_any.get_progress().percent,f2.get_progress().percent)
        
class TestProgressObserver(BackendInfraTest):
    def test_sanity(self):
        f = future.Future()
        class ProgressKeeper(object):
            def __init__(self):
                self.progress = None
            def update_method(self, progress):
                self.progress = progress
        keeper = ProgressKeeper()
        po = ProgressObserver(keeper.update_method, 10)
        def check_progress(progress):
            self.assertEqual(keeper.progress, progress)
            self.assertEqual(po.last_reported_progress, progress)
        f.attach_observer(po, b_notify_on_progress = True)
        check_progress(None)
        # First update is accepted since we have nothing
        f.set_progress(5)
        check_progress(5)
        # Second update is ignored since the change is too small
        f.set_progress(10)
        check_progress(5)
        # Now the change is big enough
        f.set_progress(15)
        check_progress(15)
        # And again
        f.set_progress(95)
        check_progress(95)
        # checking setting the future (even when the progress is close to 100)
        f.set(None)
        check_progress(100)

from unit import build_suite, run_suite, combine_suites
def suite():
    return combine_suites(
        build_suite(TestFuture), 
        build_suite(TestFutureAggregator), 
        build_suite(TestFutureAny), 
        build_suite(TestProgressObserver),
    )

if __name__ == '__main__':
    run_suite(suite())
