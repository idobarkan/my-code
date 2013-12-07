try:
    from unittest2 import TestCase
    from unittest2.suite import TestSuite
    from unittest2.runner import TextTestResult, _WritelnDecorator, TextTestRunner

except ImportError:
    from unittest import TestCase
    from unittest.suite import TestSuite
    from unittest.runner import TextTestResult, _WritelnDecorator, TextTestRunner    

import sys
from util import ObjectAggregator, fmt_exc #@UnresolvedImport
from DTO import DTO
from xunit import Xunit
from hashlib import md5
import copy

b_run_forever = False
global_filter_names = None
b_throw_errors = True

if 'Xforever' in sys.argv:
    b_run_forever = True
    sys.argv.remove('Xforever')

def md5_hash(s):
    """ We can't use builtin hash since this is framework specific and will give different results for .net 32 and 64
    """
    m = md5()
    m.update(s)
    return int(m.hexdigest(), 16)

def chunks(l, n):
    """ Yield successive n-sized chunks from l."""
    for i in xrange(0, len(l), n):
        yield l[i:i+n]

def test_labels(*labels):
    """A decorator for test methods that classifies the test with one or more labels.
       The labels should normally be strings.
    """
    def deco(f):
        f.test_labels = set(labels)
        return f
    return deco

def get_global_filters():
    if global_filter_names is not None:
        return global_filter_names
    if len(sys.argv) > 1:
        return sys.argv[1:]
    return []
    
def build_suite(cls,prefix='test_', whitelist=None, blacklist=None, b_check_names=True, b_check_labels=True):
    whitelist = set(whitelist if whitelist is not None else [])
    blacklist = set(blacklist if blacklist is not None else [])
    
    global_filters = get_global_filters()
    
    # extract filters_slice (if any) from global filters
    filters_slice = None
    if global_filters and global_filters[0] == '*':
        n_inst = int(global_filters[1])
        n_count = int(global_filters[2])
        filters_slice = (n_inst,n_count)
        global_filters = global_filters[3:]
    
    # extract white and black lists from global_filters
    blacklist_prefix = '-no_'
    for name in global_filters:
        if name.startswith(blacklist_prefix):
            blacklist.add( name[len(blacklist_prefix):] )
        else:
            whitelist.add(name)
            
    # if filters_slice is active, narrow the list to relevant filters_slice
    st_filtered_names = set(filter(lambda x: x.startswith(prefix) and callable(getattr(cls, x)), dir(cls)))
    if filters_slice is not None:
        n_inst, n_count = filters_slice
        new_names = set()
        for test_name in st_filtered_names:
            if md5_hash('%s.%s' % (cls.__name__,test_name)) % n_count == n_inst:
                new_names.add(test_name)
        st_filtered_names = new_names

    def find_matches(test_names, st_filters):
        matches = set()
        for test_name in test_names:
            # check if name matches
            if b_check_names:
                for name in st_filters:
                    if name in test_name:
                        matches.add(test_name)

            # check if label matches
            if b_check_labels:
                mth = getattr(cls,test_name)
                test_labels = getattr(mth,'test_labels',set())
                if st_filters & test_labels:
                    matches.add(test_name)
        return matches
    
    # if we have black-lists, keep only tests that don't match them
    st_filtered_names -= find_matches(st_filtered_names,blacklist)
    
    # if we have white-lists of names or labels, take only subset of tests that match them
    if whitelist:
        st_filtered_names = find_matches(st_filtered_names,whitelist) 

    # done with filtering - build the TestSuite    
    return TestSuite(cls(test_name) for test_name in st_filtered_names)

def combine_suites(*suites):
    lst_suites = list(suites)
    return TestSuite(lst_suites)

def my_import(name):    
    '''taken from python documentation on __import__ builtin function. more info there.'''
    mod = __import__(name)
    components = name.split('.')
    for comp in components[1:]:
        mod = getattr(mod, comp)
    return mod

def package_suite(module_names,prefix='test_'):
    s = TestSuite()
    for name in module_names:
        mod = my_import(prefix+name)
        s.addTest(mod.suite())
    return s

import time
class EnhancedTextTestResult(TextTestResult):
    def __init__(self, stream, descriptions, verbosity, immediate_stream):
        super(EnhancedTextTestResult, self).__init__(stream, descriptions, verbosity)
        self.xunit = Xunit('TestResults.xml')
        self.xunit._exc_info_to_string = self._exc_info_to_string
        self.immediate_stream = _WritelnDecorator(immediate_stream)
        self.last_test = None

    def _exc_info_to_string(self, err, test):
        """Converts a sys.exc_info()-style tuple of values into a string."""
        orig = super(EnhancedTextTestResult, self)._exc_info_to_string(err, test)
        _, exc, _ = err
        formatted = "raw_exception=%s\nformatted_exception=%s" %(orig, fmt_exc(exc))
        if len(formatted.split('\n')) <=2:
            return orig
        else:
            return formatted

    def addError(self, test, err):
        super(EnhancedTextTestResult, self).addError(test, err)
        self.xunit.addError(test, err)
        self.write_to_file('ERROR', test, err)
        
    def addFailure(self, test, err):
        super(EnhancedTextTestResult, self).addFailure(test, err)
        self.xunit.addFailure(test, err)
        self.write_to_file('FAIL', test, err)

    def addSuccess(self, test):
        super(EnhancedTextTestResult, self).addSuccess(test)
        self.xunit.addSuccess(test)
        
    def startTest(self, test):
        super(EnhancedTextTestResult, self).startTest(test)
        self.xunit.startTest(test)
        
    def stopTest(self, test):
        super(EnhancedTextTestResult, self).stopTest(test)
        self.xunit.stopTest(test)
        
    def write_to_file(self, flavour, test, err):
        try:
            if str(test) != self.last_test:
                if self.last_test is not None:
                    self.immediate_stream.writeln("<</TestMethod>>")
                self.immediate_stream.writeln("<<TestMethod %s" % (self.getDescription(test),))
            self.immediate_stream.writeln(self.separator1)
            self.immediate_stream.writeln("%s: %s" % (flavour,self.getDescription(test)))
            self.immediate_stream.writeln(self.separator2)
            exc_string = self._exc_info_to_string(err, test)
            exc_string = exc_string.replace('\r\n','\n') # prints better on notepad++
            self.immediate_stream.writeln("%s" % exc_string)
            self.immediate_stream.flush()
        except:
            print 'Error writing to immediate stream'
        finally:
            self.last_test = str(test)

class EnhancedTextTestRunner(TextTestRunner):
    def __init__(self, *a, **kw):
        super(EnhancedTextTestRunner, self).__init__(*a, **kw)
        self.result = None
        persistent_stream = file('TestResults.run', mode='a+' ,buffering = 0)
        try:
            persistent_stream.write('<</TestSuite>> <</TestSuite>> <</TestSuite>> <</TestSuite>>\n')
            persistent_stream.write('<<TestSuite Test started on %s>>\n' % (time.ctime(time.time()),))
            persistent_stream.flush()
        except:
            print 'Error writing to immediate stream'
        self.streams = ObjectAggregator([persistent_stream,
                                         file('LatestTestResults.run', mode='w' ,buffering = 0)])
    def _makeResult(self):
        self.result = EnhancedTextTestResult(self.stream, self.descriptions, self.verbosity, self.streams)
        return self.result

 
runner = EnhancedTextTestRunner(verbosity=2)

def run_suite(suite):
    print 'Running start time %s' % (time.ctime(time.time()),)
    rc = runner.run(suite)
    
    if b_run_forever:
        run_number = 1
        while(rc.wasSuccessful()):
            run_number += 1
            print 'Running (iteration %s). start time %s' % (run_number, time.ctime(time.time()))
            rc = runner.run(suite)
        
    try: 
        runner.result.xunit.report()
    except Exception,e : 
        print e
    if not rc.wasSuccessful():
        print 'XX XX XX SOME TESTS FAILED XX XX XX' # This text is used by hudson to fail the build
        print "\n*** Rerun ***\ngo testbe %s\n" % " ".join(test_names_from_err(rc.errors+rc.failures))
        
def print_errors():
    if runner and runner.result and not runner.result.wasSuccessful():
        runner.result.printErrors()
        print "\n*** Rerun ***\ngo testbe %s" % " ".join(test_names_from_err(runner.result.errors+runner.result.failures))
    else:
        print "\nNo errors"
    
def test_names_from_err(errors):
    errs = [error[0].__str__() for error in errors]
    # remove repetitions
    names = set(err[len('test_'):err.index(' ')] for err in errs)
    return names

#################################
# Variations
#################################
class TestVariationsMeta(type):
    """Make this class the metaclass for your test suite in order to enable the test_variations decorator (see below)     
    """
    def __new__(mcls, classname, bases, class_dict): #@NoSelf
        for name, obj in class_dict.items():
            test_prefix = 'test_'
            if name.startswith(test_prefix) and hasattr(obj,'test_variations'):
                mth = obj
                short_name = name[len(test_prefix):]
                for variation in mth.test_variations:
                    dct_new_methods = variation(short_name,mth)
                    for new_name,new_mth in dct_new_methods.iteritems():
                        labels = copy.copy(getattr(mth,'test_labels',set()))
                        labels.add('variation')
                        new_mth.test_labels = labels 
                        class_dict[test_prefix + 'variation_' + new_name] = new_mth
        return type.__new__(mcls,classname, bases, class_dict)
    
def test_variations(*a):
    """Use this decorator to specify that a test method should also have "variations".
       Each argument to the decorator should be a variation object v, such that calling v(test_name,test_method)
       returns a dictionary {test_name -> test_method} with additional test methods that should be added to the suite.
       Usually these methods will change some context and then call the original method.
    """
    def deco(f):
        f.test_variations = a
        return f
    return deco

#################################
# TestCase
#################################
class TestCase(TestCase):
    __metaclass__ = TestVariationsMeta
    def __init__(self, methodName='runTest'):
        super(TestCase, self).__init__(methodName = methodName)
    
    def assertDTOEqual(self, dto1, dto2, msg=None):
        self.assertTrue(isinstance(dto1, DTO), 'First argument is not a DTO')
        self.assertTrue(isinstance(dto2, DTO), 'Second argument is not a DTO')
        self.assertDictEqual(dto1._to_dct(), dto2._to_dct(), msg = msg)
            
    def assertEqual(self, first, second, msg=None):
        if isinstance(first, DTO) and isinstance(second, DTO):
            self.assertDTOEqual(first, second, msg = msg)
        else:
            super(TestCase, self).assertEqual(first, second, msg = msg)