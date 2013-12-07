from test_infra_base import BackendInfraTest
import util
from assertions import AssertionException
from stopwatch import Stopwatch
from validations import validate_ip_string
from datetime import datetime, timedelta
from util import total_seconds, total_milliseconds, total_minutes
from time import sleep
import threading

class TestSynchronized(BackendInfraTest):
    def setUp(self):
        super(TestSynchronized,self).setUp()
        
        class Synched(object):
            def __init__(self, sleep_time_sec):
                self._lock = util.RLock() # used by @synchronized() decorator
                self.sleep_time_sec = sleep_time_sec
                self.x = 0

            def add(self,y):
                tmp = self.x
                sleep(self.sleep_time_sec)
                self.x += y
                return tmp

            @util.synchronized()
            def sync_add(self, y):
                return self.add(y)

        self.s = Synched(1)
        self.stopwatch = Stopwatch()
        
    def test_normal(self):
        self.stopwatch.start()
        threading.Thread(target=util.curry(self.s.sync_add, 10)).start()
        sleep(0.05) # make sure other thread gets head start (and the mutex)
        val = self.s.sync_add(5)
        self.assertEqual(val, 10)
        
        duration = self.stopwatch.duration()
        self.assert_(duration > 1.9*self.s.sleep_time_sec, 'calls completed too quickly. duration=%s' % duration)

    def test_no_sync(self):
        self.stopwatch.start()
        threading.Thread(target=util.curry(self.s.add, 10)).start()
        sleep(0.05)
        val = self.s.add(5)
        self.assertEqual(val, 0)
        
        duration = self.stopwatch.duration()
        self.assert_(duration < 1.3*self.s.sleep_time_sec, 'calls took too long. duration=%s' % duration)

class TestCache(BackendInfraTest):
    def setUp(self):
        super(TestCache,self).setUp()
        
        class A(object):
            def __init__(self):
                self.n_calls = 0
            
            @util.cache
            def add(self,x,y):
                self.n_calls += 1
                return x+y

            @util.cache
            def sub(self,x,y):
                self.n_calls += 1
                return x-y

            @util.cache
            def echo(self,x):
                self.n_calls += 1
                return x
                
        self.a = A()
                
    def test_sanity(self):        
        # first call not in cache
        sum_ = self.a.add(2,3)
        self.assertEqual(sum_,5)
        self.assertEqual(self.a.n_calls,1)
        
        # second call already in cache
        sum_ = self.a.add(2,3)
        self.assertEqual(sum_,5)        
        self.assertEqual(self.a.n_calls,1)
        
        # call with different args - not in cache
        sum_ = self.a.add(2,4)
        self.assertEqual(sum_,6)
        self.assertEqual(self.a.n_calls,2)

        # call both sets of args again - both should still be in cache
        sum_ = self.a.add(2,3)
        self.assertEqual(sum_,5)
        sum_ = self.a.add(2,4)
        self.assertEqual(sum_,6)
        self.assertEqual(self.a.n_calls,2)

    def test_separate_caches(self):
        # prime cache for add() and verify it
        sum_ = self.a.add(2,3)
        self.assertEqual(sum_,5)
        self.assertEqual(self.a.n_calls,1)
        sum_ = self.a.add(2,3)
        self.assertEqual(sum_,5)
        self.assertEqual(self.a.n_calls,1)
        
        # verify cache for sub() is different and also works
        diff = self.a.sub(2,3)
        self.assertEqual(diff,-1)
        self.assertEqual(self.a.n_calls,2)
        diff = self.a.sub(2,3)
        self.assertEqual(diff,-1)
        self.assertEqual(self.a.n_calls,2)
        
    def test_kwargs(self):
        # first call
        diff = self.a.sub(x=3,y=2)
        self.assertEqual(diff,1)
        self.assertEqual(self.a.n_calls,1)

        # another call with same kwargs uses cache
        diff = self.a.sub(x=3,y=2)
        self.assertEqual(diff,1)
        self.assertEqual(self.a.n_calls,1)
        
        # call with different order also uses cache
        diff = self.a.sub(y=2,x=3)
        self.assertEqual(diff,1)
        self.assertEqual(self.a.n_calls,1)
        
        # call with different args/kwargs mix is considered different call
        diff = self.a.sub(3, y=2)
        self.assertEqual(diff,1)
        self.assertEqual(self.a.n_calls,2)
        
        # another call to this variant now uses cache
        diff = self.a.sub(3, y=2)
        self.assertEqual(diff,1)
        self.assertEqual(self.a.n_calls,2)
        
    def test_none(self):
        # baseline - echo simple integer
        x = self.a.echo(3)
        self.assertEqual(x,3)
        self.assertEqual(self.a.n_calls,1)
        x = self.a.echo(3)
        self.assertEqual(x,3)
        self.assertEqual(self.a.n_calls,1)

        # check with None
        x = self.a.echo(None)
        self.assertEqual(x,None)
        self.assertEqual(self.a.n_calls,2)
        x = self.a.echo(None)
        self.assertEqual(x,None)
        self.assertEqual(self.a.n_calls,2)

    def test_dct(self):
        # limitation - doesn't work with arguments that aren't hashable
        d = {1:2}
        self.assertRaises(TypeError,self.a.echo,d)        

class TestUtilFunctions(BackendInfraTest):
    def test_sub_dict(self):
        d = {1: 'john', 2:'mary'}
        sd = util.sub_dict(d, [2,3])
        self.assertEqual(sd,{2:'mary', 3:None})
        self.assertRaises(KeyError,util.sub_dict, d, [2,3], b_allow_missing=False)
        
    def test_time_parse(self):
        iso_time = "01:02:03 PM"
        dt = util.parse_time(iso_time)
        self.assertEqual(dt.hour, 13)
        self.assertEqual(dt.minute, 2)
        self.assertEqual(dt.second, 3)
        
    def test_iso_parse(self):
        iso_time = "2003-09-25T10:49:41.987000"
        dt = util.parse_iso8601(iso_time)
        self.assertEqual(dt, datetime(2003, 9, 25, 10, 49, 41, 987000))
        
    def test_dict_exclude(self):
        d = {1: 'john', 2:'mary'}
        sd = util.dict_exclude(d,[1])
        self.assertEqual(sd,{2:'mary'})
    
    def test_dict_combine(self):
        d1 = {1: 'john', 2:'mary'}
        d2 = {3: 'aaa', 4:'bbb'}
        d,st_intersect = util.dict_combine(d1,d2)
        self.assertEqual(st_intersect,set())
        self.assertEqual(d,{1: 'john', 2:'mary',3: 'aaa', 4:'bbb'})
        d2 = {2: 'aaa', 4:'bbb'}        
        d,st_intersect = util.dict_combine(d1,d2)
        self.assertEqual(st_intersect,set([2]))
        self.assertEqual(d,{1: 'john', 2:'aaa', 4:'bbb'})        

    def test_double_diff(self):
        want = (2*x for x in range(3)) # check iterable. [0,2,4]
        have = [1,5,2,4,1] # check duplicates in input
        to_add, to_remove = util.double_diff(have,want)
        self.assertEqual(to_add,set([0]))
        self.assertEqual(to_remove,set([1,5]))

    def test_dict_diff(self):
        d1 = {1:1, 2:2, 3:3}
        d2 = {4:4,1:11}
        added,removed,changed = util.dict_diff(d1,d2)
        self.assertEqual(added,set([4]))
        self.assertEqual(removed,set([2,3]))
        self.assertEqual(changed,set([1]))
        
        # check calling with None for d1
        added,removed,changed = util.dict_diff(None,d2)
        self.assertEqual(added,set([1,4]))
        self.assertEqual(removed,set())
        self.assertEqual(changed,set())

        # check calling with None for d2
        added,removed,changed = util.dict_diff(d1,None)
        self.assertEqual(added,set())
        self.assertEqual(removed,set([1,2,3]))
        self.assertEqual(changed,set())
    
    def test_curry(self):
        def add(x,y,z):
            return 100*x+10*y+z
        c = util.curry(add,1,z=3)
        self.assertEqual(c(2),123)

    def test_sanitize_user_input(self):
        self.assertEqual(util.sanitize_user_input("ABCDEFG1234"),"ABCDEFG1234")
        self.assertEqual(util.sanitize_user_input("ABCDEFG 1234"),"ABCDEFG-1234")
        self.assertEqual(util.sanitize_user_input("ABCDEFG-1234"),"ABCDEFG-1234")
        self.assertEqual(util.sanitize_user_input("ABCDEFG 1234 %%$$##"),"ABCDEFG-1234-------")
        self.assertEqual(util.sanitize_user_input("12%S%%BCDEFG 1234 %%$$##"),"12-S--BCDEFG-1234-------")
        
    def test_dicts_to_csv(self):
        filename = 'test_dicts_to_csv.csv'
        util.dicts_to_csv([],filename)
        self.assertEqual(file(filename,'r').readlines(),[])
        util.dicts_to_csv([{'a':1,'b':2},{'b':5,'a':'ad'}],filename)
        self.assertEqual(file(filename,'r').readlines(),['a,b,\n', '1,2,\n', 'ad,5,\n'])
        
    def test_defaultdict(self):
        from collections import defaultdict as old_dd
        from util import defaultdict as new_dd
        old_d= old_dd(list)
        new_d = new_dd(list)
        self.assertEqual(old_d, new_d)
        self.assertEqual(old_d[0], new_d[0])
        self.assertEqual(old_d, new_d)
        self.assertEqual(old_d.pop(0), new_d.pop(0))
        self.assertEqual(old_d, new_d)
        
    def test_create_random_password(self):
        capitals = [chr(x) for x in xrange(ord('A'), ord('Z') + 1)]
        letters = [chr(x) for x in xrange(ord('a'), ord('z') + 1)]
        digits = [str(x) for x in xrange(10)]
        for x in xrange(100):
            password = util.create_rand_password(10)
            self.assert_(password[0] in capitals)
            self.assert_(password[1] in letters)
            self.assert_(password[2] in digits)
            self.assertEqual(len(password), 10)
        # Check length limits 
        util.create_rand_password(3)
        self.assertRaises(Exception, util.create_rand_password,2)
    
    def test_flatten_params(self):
        self.assertEqual(util.flatten_params('a'),"'a'")
        self.assertEqual(util.flatten_params(1),"1")
        self.assertEqual(util.flatten_params([1]),"[1]")
        self.assertEqual(util.flatten_params({'x':1}),"dict(x=1, )")
        self.assertEqual(util.flatten_params(util.Bunch(x=1)),"Bunch(x=1, )")
        self.assertEqual(util.flatten_params(util.Bunch(x=1,y={'z':util.Bunch(a=1)})),"Bunch(x=1, y=dict(z=Bunch(a=1, ), ), )")
        
    def test_get_ip_for_target(self):
        ip = util.get_ip_for_target(("betest", 8080))
        validate_ip_string(ip)
        
    def test_time_conversions(self):
        now = datetime.now()
        self.assertEqual(now, util.from_dotnet_datetime(util.to_dotnet_datetime(now)))
        
    def test_calculate_net_time(self):
        # sanity 
        now = datetime.now()
        def time(i):
            res = now + timedelta(seconds=i)
            return res
        
        def time_seg(s,e):
            return (time(s),time(e))
        
        # sanity
        net_time = util.calculate_net_time(time(0), time(10), [ time_seg(5,9)])
        self.assertEqual(net_time, 6*1000)
        net_time = util.calculate_net_time(time(0), time(100), [ time_seg(53,93)])
        self.assertEqual(net_time, 60*1000)                        
        net_time = util.calculate_net_time(time(0), time(20), [ time_seg(1,3), time_seg(5,8) , time_seg(10,11), time_seg(15,18)])
        self.assertEqual(net_time, (20-2-3-1-3)*1000)
        
        # parallelism 
        net_time = util.calculate_net_time(time(0), time(20), [ time_seg(1,10), time_seg(5,20)] )
        self.assertEqual(net_time, 1*1000) # was active only for one second
        net_time = util.calculate_net_time(time(0), time(20), [ time_seg(1,3), time_seg(2,4) , time_seg(10,18), time_seg(12,13),time_seg(12,17),time_seg(17,18),time_seg(15,19)] )
        self.assertEqual(net_time, (1+6+1)*1000) # was active between 0-1,4-10,19-20
        
        # edge cases
        net_time = util.calculate_net_time(time(0), time(20), [ time_seg(1,10), time_seg(5,25)] )
        self.assertEqual(net_time, 1*1000) # was active only for one second
        net_time = util.calculate_net_time(time(0), time(20), [ time_seg(0,6), time_seg(6,21)] )
        self.assertEqual(net_time, 0*1000)
        
    def test_total_seconds_and_total_milliseconds(self):
        year = timedelta(days=365)                        
        year_total_seconds = total_seconds(year)
        self.assertEqual(type(year_total_seconds), float, "expected float type")
        self.assertEqual(year_total_seconds, 31536000.0)
        self.assertEqual(total_milliseconds(year), 31536000.0 * 1000)
        self.assertEqual(total_minutes(year), 365 * 24 * 60)
        self.assertEqual(total_seconds(year*2), 31536000.0 *2)
        y = timedelta(days=365, minutes=55, seconds=444, microseconds=33)
        self.assertEqual(total_seconds(y), (365 * 24 * 60 * 60) + (55 * 60) + 444 + (33.0 / 10**6) )
        self.assertEqual(total_milliseconds(y), total_seconds(y) * 1000)
        self.assertEqual(total_minutes(y) * 60, total_seconds(y))
    
class TestSetMembers(BackendInfraTest):
    def test_normal(self):
        class A(util.DTO):
            def __init__(self,x,y):
                super(A,self).__init__(locals())
                
        a = A(x=3,y='fred')
        self.assertEqual(a.x,3)
        self.assertEqual(a.y,'fred')

class TestMathUtils(BackendInfraTest):
    def test_double_cmp(self):
        self.assertEqual(util.double_cmp(1.0,2.3),False)
        self.assertEqual(util.double_cmp(1.2,1.2),True)
        self.assertEqual(util.double_cmp(1.5,3.0/2),True)
        self.assertEqual(util.double_cmp(1.5,1.50003),False)
        self.assertEqual(util.double_cmp(1.5,1.5+1E-7),True)        
        
    def test_mean_stddev(self):
        mean,stddev = util.calc_mean_stddev([1,1,1,1,1,1,1,1,1])
        self.assert_(util.double_cmp(mean,1.0),"mean=%s" % (mean,))
        self.assert_(util.double_cmp(stddev,0.0),"stddev=%s" % (stddev,))        

        mean,stddev = util.calc_mean_stddev([1,2,3])
        self.assert_(util.double_cmp(mean,2.0),"mean=%s" % (mean,))
        self.assert_(util.double_cmp(stddev,1.0),"stddev=%s" % (stddev,)) 
        
    def test_uniform_choice(self):
        n = 10 ** 4
        def run_many(dct_probabilities):
            dct_count = dict( (key,0) for key in dct_probabilities.iterkeys() )
            for _ in xrange(n):
                res = util.uniform_choice(dct_probabilities)
                self.assert_(res in dct_count)
                dct_count[res] +=1
            return dct_count
        # sanity
        dct_count = run_many({1:30,2:60,3:120})
        self.assert_(dct_count[1] * 1.5 < dct_count[2])
        self.assert_(dct_count[2] * 1.5 < dct_count[3])
        # with zeros
        dct_count = run_many({1:0,2:33,3:66,4:0})
        self.assertEqual(dct_count[1],0)
        self.assertEqual(dct_count[4],0)
        self.assertEqual(dct_count[2] + dct_count[3],n)
        self.assert_(dct_count[2] * 1.5 < dct_count[3])
        # all zeros
        self.assertRaises(AssertionException,run_many,{1:0,2:0,3:0})
        # negative values
        self.assertRaises(AssertionException,run_many,{1:40,2:50,3:-1})
        
    def test_get_normalized_progress(self):
        def check_lst(lst,expected_res):
            res = util.get_normalized_progress(lst)
            self.assertEqual(res,expected_res)
        
        check_lst([],0) 
        check_lst([(1,100),(2,100),(10,100),(34,100)],100) 
        check_lst([(1,100),(1,100),(2,0)],50) 
        check_lst([(1,50),(2,50),(3,0)],25) 
        check_lst([(50,26),(10,100),(10,0),(20,30),(10,90)],38) 
        
class TestImport(BackendInfraTest):
    def test_import(self):
        x = util.simple_import('infra.tests.test_util')
        from infra.tests import test_util
        self.assert_(x is test_util,"Expected %s. got %s" % (test_util,x))
  
class TestPlotData(BackendInfraTest):
    def test_plot_data(self):
        f = file('test.prop','w')
        f.write('YVALUE=4\nURL=http://foo.bar/\n')
        f.close()
        f = file('test.csv', 'w')
        f.write("""Avg,Median,90,min,max,samples,errors,error %
515.33,196,1117,2,16550,97560,360,0.37""")
        f.close()
        
from unit import build_suite, run_suite, combine_suites
def suite():    
    return combine_suites(
        build_suite(TestUtilFunctions),
        build_suite(TestSynchronized),
        build_suite(TestCache),
        build_suite(TestSetMembers),
        build_suite(TestMathUtils),
        build_suite(TestImport),
        build_suite(TestPlotData),
    )

if __name__ == '__main__':
    run_suite(suite())
