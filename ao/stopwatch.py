import time

class Stopwatch(object):
    def __init__(self):
        self.start()
        
    def start(self):
        self.start_seconds = time.clock()
        
    def duration(self):
        return time.clock() - self.start_seconds
    
    def duration_milliseconds(self):
        return (time.clock() - self.start_seconds) * 1000

    def __str__(self):
        return str(self.duration())
    def __repr__(self):
        return str(self.duration())
                
def time_it(f, *a, **kw):
    s = Stopwatch()
    x = f(*a, **kw)
    return x, s.duration()

class TimeProbe(object):
    def __init__(self, name):
        self._watch = Stopwatch()
        self.probe_list = []
        self.name = name
        self.probe_list.append(('init', 0))
        
    def probe(self, stage):
        total_duration = self._watch.duration()
        stage_duration = total_duration - self.probe_list[-1][1]
        self.probe_list.append((stage, total_duration))
        return (stage_duration, total_duration)
        
    def restart(self):
        self._watch.start()
        self.probe_list = []
        
    def __str__(self):
        res = 'TimeProbe for %s: init' % self.name
        _,last_duration = self.probe_list[0]
        for probe in self.probe_list[1:]:
            current_stage, current_duration = probe
            diff_duration = current_duration - last_duration
            res += ', %s=%s' % (current_stage, diff_duration)
            _,last_duration = probe
        res += ', Total=%s' % self.probe_list[-1][1]
        return res