import __builtin__
import threading
import subprocess
import gc
from subprocess import PIPE
from tempfile import NamedTemporaryFile
import iso8601
    
def dotnet_import(module, lst_symbols=None):
    try:
        return __import__(module, fromlist=lst_symbols)
    except:
        return None

import random
import hashlib
import base64
import socket
import pickle
import string
from StringIO import StringIO
from datetime import datetime
from dynamic_proxy import DynamicProxy 
from DTO import DTO, Bunch, BunchKw, Anything #@UnusedImport
from exception_utils import convert_exceptions, fmt_exc #@UnusedImport
from null_object import NullObject #@UnusedImport
import assertions
DotNetSystem = dotnet_import("System", ["GC", "DateTime"])
from dateutil import parser

def parse_time(time_value):
    return parser.parse(time_value)

def parse_iso8601(time_value):
    return iso8601.parse_date(time_value, default_timezone=None)

#####################################
# Synchronized
#####################################

class RLock(object):
    def __init__(self):
        self.lock = threading.RLock()
    def acquire(self):
        self.lock.acquire()
    def release(self):
        self.lock.release()
        
    def __enter__(self):
        self.acquire()
        
    def __exit__(self, t, v, tb): #@UnusedVariable
        self.release()

def synchronized(lock = None):  
    def deco(f):
        '''Method decorator, which surrounds decorated method with
        Requires that self._lock on host object return the lock'''
        def _wrapped(self,*a,**kw):
            _lock = lock if lock is not None else self._lock
            with _lock:#synchronize_with(_lock):
                return f(self,*a,**kw)
        _wrapped.__name__ = f.__name__
        return _wrapped
    return deco 

#####################################
# Cache
#####################################
def cache(f):
    """Caches pure functions. Requires arguments to be hashable"""
    dct = {} # holds cache results { (args,kwargs) -> result }
    def _wrapped(*a,**kw):
        key = (a,tuple(sorted(kw.items())))
        if key in dct:
            return dct[key]
        else:
            res = f(*a,**kw)
            dct[key] = res
            return res
    _wrapped.__name__ = f.__name__
    return _wrapped    

#####################################
# Pickle extension
#####################################

def pickle_ex(obj, persistent_id = None):
    sio = StringIO()
    pickler = pickle.Pickler(sio)
    if persistent_id:
        pickler.persistent_id = persistent_id
    pickler.dump(obj)
    res = sio.getvalue()
    sio.close()
    return res
                         
def unpickle_ex(s, persistent_load = None):
    sio = StringIO(s)
    unpickler = pickle.Unpickler(sio)
    if persistent_load:
        unpickler.persistent_load = persistent_load
    obj = unpickler.load()
    sio.close()
    return obj

#####################################
# ObjectAggregator
#####################################
class ObjectAggregator(DynamicProxy):
    def __init__(self, objects):
        self.objects = objects
    
    def _is_callable(self, name):
        return callable(getattr(self.objects[0], name))

    def _get_property(self, name):
        return [getattr(obj, name) for obj in self.objects]
    
    def _dispatch(self, method_name, *a, **kw):
        for obj in self.objects:
            method = getattr(obj, method_name)
            method(*a, **kw)       

def sub_dict(d, keys, b_allow_missing=True):
    if b_allow_missing:
        return dict((k,d.get(k)) for k in keys)
    else:
        return dict((k,d[k]) for k in keys)

def dict_exclude(d,excluded):
    return dict((k,v) for k,v in d.iteritems() if k not in excluded)

def dict_combine(d1,d2):
    """ Return combined dict and the intersection set of the two sets of keys """
    st_intersect = set(d1.keys()).intersection(set(d2.keys()))
    u_dict = dict(d1.items() + d2.items())
    return u_dict,st_intersect

def double_diff(seq1,seq2):
    """Returns pair of sets (added,removed) showing changes from seq1 to seq2"""
    s1 = set(seq1)
    s2 = set(seq2)
    added = s2-s1
    removed = s1-s2
    return added,removed

def dict_diff(d1,d2):
    """ Both d1 and d2 should be dictionaries. None is allowed, and treated as empty dictionary.
        Returns tuple (added,removed,changed) keys when going from d1 to d2.
    """
    if d1 is None: d1 = {}
    if d2 is None: d2 = {}
    added = set(k2 for k2 in d2.iterkeys() if k2 not in d1)
    removed = set()
    changed = set()
    for k1,v1 in d1.iteritems():
        if k1 in d2:
            v2 = d2[k1]
            if v2 != v1:
                changed.add(k1)
        else:
            removed.add(k1)
    return (added,removed,changed)

def curry(f,*bind_a,**bind_kw):
    def curried(*a,**kw):
        all_kw = bind_kw.copy()
        all_kw.update(kw)
        return f(*(bind_a+a),**all_kw)
    return curried

import math        
def calc_mean_stddev(seq):
    lst = list(seq)
    n = len(lst)
    mean = sum(lst)/n
    variance = sum((x-mean)**2 for x in lst) / (n-1)
    stddev = math.sqrt(variance)
    return (mean,stddev)
    
def double_cmp(x,y):
    epsilon = 1E-6
    return abs(x-y) < epsilon

def uniform_choice(dct_probabilities):
    for weight in dct_probabilities.itervalues():
        assertions.fail_if(weight<0, "cannot have negative weight as a probability", dct_probabilities=dct_probabilities)
    epsilon = 1E-6
    weight_sum = sum(dct_probabilities.itervalues())
    assertions.fail_unless(weight_sum>0, "must have at least one non 0 probability", dct_probabilities=dct_probabilities)      
    choice_point = random.random() * weight_sum
    sum_so_far = 0.0
    for key,weight in dct_probabilities.iteritems():
        sum_so_far += weight
        if sum_so_far + epsilon > choice_point:
            return key
    assertions.fail("should not reach here, probably bug in the choosing algorithm")

def get_normalized_progress(lst_progress_weights):
    total_weight = sum(weight for weight,progress in lst_progress_weights)
    res = 0
    if total_weight == 0:
        return res
    for weight,progress in lst_progress_weights:
        res += (float(weight) / total_weight) * progress
    return int(round(res))

def simple_import(name):
    mod = __builtin__.__import__(name)
    # in case of dotted name, return last module, not first as __import__ does
    components = name.split('.')   
    for c in components[1:]:
        mod = getattr(mod, c)
    return mod
    
def has_spaces(_str):
    return _str.find(' ') != -1
    
def sanitize_spaces(_str):
    return _str.strip().replace(' ','-')

def sanitize_user_input(_str):
    legal_chars = string.digits + string.ascii_letters
    st_tran = set(x for x in _str if x not in legal_chars)
    frm = ''.join(st_tran)
    to = '-'* len(frm)
    return _str.translate(string.maketrans(frm,to))      

def get_short_string_from_obj(obj, max_len):
    str_obj = str(obj)
    if len(str_obj) > max_len:
        str_obj = str_obj[:max_len] + '...'
    return str_obj

def dicts_to_csv(dicts, filename):
    f = file(filename, 'w+')
    try:
        if not dicts:
            return
        # make headers
        d = dicts[-1]
        keys = sorted(d.keys())
        for k in keys:
            f.write('%s,' % (k,))
        f.write('\n')
        for d in dicts:
            for k in keys:
                f.write('%s,' % (d.get(k) if d.get(k) is not None else '',))
            f.write('\n')
    finally:
        f.close()

        
def run_command(args):
    if DotNetSystem is None:
        # cpython
        stdout = NamedTemporaryFile()
        stderr = NamedTemporaryFile()
        res = subprocess.call(args, stdin=PIPE, stdout=stdout, stderr=stderr)
        return stdout.read(), stderr.read(), res        
    else:
        # IronPython
        stdout = StringIO()
        stderr = StringIO()
        res = subprocess.call(args, stdin=PIPE, stdout=stdout, stderr=stderr)
        return stdout.getvalue(), stderr.getvalue(), res
    

def TEST_get_objects_with_ids():
    """ Retrieves all the objects that have assigned id by the Ipy infrastructure.
        Do not use in real code.
    """
    res = []
    import clr #@Reimport @UnresolvedImport
    clr.AddReference('Microsoft.Dynamic')
    from Microsoft.Scripting.Runtime import IdDispenser #@UnresolvedImport
    from System.Reflection import BindingFlags #@UnresolvedImport 
    hashtable = clr.GetClrType(IdDispenser).GetField('_hashtable', BindingFlags.NonPublic | BindingFlags.Static).GetValue(clr.GetClrType(IdDispenser))
    py_hash = dict(hashtable)
    for key in py_hash:
        obj = key.GetType().GetProperty('Target').GetValue(key,None)
        if obj is not None:
            res.append((id(obj), obj))
    res = sorted(res)
    return res

def create_rand_password(length):
    # create the character range - using only alphanumeric characters
    # the numbers 0-9 appear multiple times to increase the chances of having
    # numbers _and_ letters in the generated password, hence being more compliant
    # with password policies
    assertions.fail_if(length < 3, "Passwords must be a minimum of 3 characters", length = length)
    # Third 3 characters are capial,non-capital and a number to comply with most password requirements
    capitals = [chr(x) for x in xrange(ord('A'), ord('Z') + 1)]
    letters = [chr(x) for x in xrange(ord('a'), ord('z') + 1)]
    digits = [str(x) for x in xrange(10)]
    password = '%s%s%s' % (random.choice(capitals), random.choice(letters), random.choice(digits))
    # Now fill the other characters
    all_chars = capitals + letters + digits * 3
    password += "".join([random.choice(all_chars) for x in xrange(length-3)])
    return password

def _get_iterator_method(o):
    if isinstance(o, DTO): return getattr(o, 'itermembers')
    if isinstance(o, dict): return getattr(o, 'iteritems')    
    return False

def flatten_params(params, str_params=''): #@UnusedVariable
    '''returns a splunk friendly string representation of a dto containing nested parameters sequences.
        e.g. util.Bunch(c='si', a=['x',4], d={1:'one',2:util.Bunch(x=['one','two'])}) '''
    m = _get_iterator_method(params)
    if not m:
        return "'%s'"%(params,) if isinstance(params, str) else str(params)
    str_params = ''
    for k,v in m():
        str_params += '%s=%s, ' % (k, flatten_params(v, str_params))
    return '%s(%s)' % (params.__class__.__name__, str_params)
   
def do_GC():
    gc.collect()

    if DotNetSystem is not None:    
        for _ in range(2):
            DotNetSystem.GC.Collect()
            DotNetSystem.GC.WaitForPendingFinalizers()

def get_current_user():
    return socket.gethostname().upper()
        
# Our own implementation of default leak since the existing for ipy is leaking JIT and slow
class defaultdict(dict):
    def __init__(self, cls):
        super(defaultdict, self).__init__()
        self.cls = cls
    def __getitem__(self, key):
        if key not in self:
            self[key] = self.cls()
        return super(defaultdict, self).__getitem__(key)

def hash_md5(s, max_chars = None):
    return base64.b32encode(hashlib.md5(str(s)).digest())[:max_chars]

def chunks(l, n):
    """ Yield successive n-sized chunks from l."""
    for i in xrange(0, len(l), n):
        yield l[i:i+n]
        
def chunk_it(seq, N):
    '''divide a sequence to N roughly equal sized chunks'''
    avg_chunk_size = len(seq) / float(N)
    result = []
    last = 0.0
    while last < len(seq):
        result.append(seq[int(last):int(last + avg_chunk_size)])
        last += avg_chunk_size
    return result

def get_ip_for_target(addr):
    """ Get the source ip that will be used to access target ip and port (both must be valid)
    """
    sock = socket.create_connection(addr)
    res = sock.getsockname()[0]
    # Cleanup
    sock.close()
    return res

def single(seq, b_allow_none=False, alert_topic=None, **kw):
    lst = list(seq)
    msg = "sequence has more than one item" if alert_topic is None else alert_topic 
    assertions.assert_that(len(lst) <= 1, msg, lst=lst, **kw)
    if not lst:
        assertions.assert_that(b_allow_none, "empty sequence not allowed")
        return None
    return lst[0]

def total_seconds(td):
    "return the equivalent of timedelta.total_seconds() in python 2.7"
    return (td.microseconds + (td.seconds + td.days * 24 * 3600) * 10**6) / float(10**6)

def total_hours(td):
    seconds = total_seconds(td) # already a float
    return seconds / 3600 if seconds else 0

def total_milliseconds(td):
    return total_seconds(td) * 1000

def total_minutes(td):
    seconds = total_seconds(td)
    return seconds / 60.0 if seconds else 0

def from_dotnet_datetime(d):
    if d is None:
        return None
    
    elif DotNetSystem is None:
        return d
    
    elif isinstance(d, datetime):
        return d
    
    elif isinstance(d, DotNetSystem.DateTime):
        return datetime(d.Year , d.Month, d.Day, d.Hour, d.Minute, d.Second, d.Millisecond * 1000)

    assertions.fail("datetime cannot be converted", d=d)

def to_dotnet_datetime(d):
    if DotNetSystem is None:
        return d

    if isinstance(d, datetime):
        milliseconds = d.microsecond / 1000 if d.microsecond!=0 else 0
        return DotNetSystem.DateTime(d.year, d.month, d.day, d.hour, d.minute, d.second, milliseconds)
    elif isinstance(d, DotNetSystem.DateTime):
        return d
    else:
        assertions.fail("unexpected datetime type %s %s" %(d, type(d),))

def calculate_net_time(start_time, end_time, lst_non_active_times):
    # sort based on start time
    lst_non_active_times.sort()
    lst_active_times = []
    last_end_time = start_time
    for child_start_time, child_end_time in lst_non_active_times:
        
        if child_start_time > last_end_time:
            lst_active_times.append((last_end_time, child_start_time))        
        last_end_time = max(child_end_time, last_end_time)
    
    if last_end_time < end_time:
        lst_active_times.append((last_end_time, end_time))

    return sum( total_milliseconds(end-start) for start,end in lst_active_times)        
        
def kill_dotnet_data(obj):
    if DotNetSystem is None:
        return obj
    elif type(obj) == DotNetSystem.Int64:
        return int(obj)
    elif type(obj) == DotNetSystem.Int32:
        return int(obj)
    elif type(obj) == DotNetSystem.String:
        return unicode(obj)
    elif isinstance(obj, dict):
        return dict((kill_dotnet_data(k), kill_dotnet_data(v)) for (k, v) in obj.iteritems())
    elif isinstance(obj, list):
        return [kill_dotnet_data(v) for v in obj]
    elif isinstance(obj, tuple):
        return tuple(kill_dotnet_data(v) for v in obj)
    elif isinstance(obj, set):
        return set(kill_dotnet_data(v) for v in obj)        
    else:
        return obj

class DotNetDataKillerAndPickler(object):
    @staticmethod
    def loads(s):
        return pickle.loads(s)
    
    @staticmethod
    def dumps(obj):
        return pickle.dumps(kill_dotnet_data(obj))

prehistory = datetime(2000,1,1)
posthistory = datetime(3000,1,1)
max_time_delta = posthistory - prehistory
