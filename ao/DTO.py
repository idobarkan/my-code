import assertions

#####################################
# DTO
#####################################

class DTO(object):
    def __init__(self,kw):
        self._instance_version = self.code_version

        d = dict(kw) # make (shallow) copy of d before changing it
        d.pop('self', None)
        clsname = type(self).__name__
        if clsname in d and d[clsname]==type(self): # side effect of using super(A,self).__init__(locals()) in subclass - A shows up in locals (ironpython only?)
            d.pop(clsname)

        self._DTO_members = d.keys()
        self._DTO_members.sort()
        for name,val in d.iteritems():
            setattr(self,name,val)

    @property
    def code_version(self): 
        return getattr(type(self), '_code_version', 0)

    @property
    def instance_version(self): 
        return getattr(self, '_instance_version', 0)

    @instance_version.setter
    def instance_version(self,val): #PyFlakesIgnore
        self._instance_version = val

    def _add_DTO_member(self,name):
        """Used internally. deprecated for use in upgrade scripts. use DTO_add_field instead"""
        assertions.fail_if(name in self._DTO_members,'name already in _DTO_members',name=name,members=self._DTO_members)
        self._DTO_members.append(name)
        self._DTO_members.sort()

    def _remove_DTO_member(self,name):
        """Used internally. deprecated for use in upgrade scripts. use DTO_remove_field instead"""
        assertions.fail_unless(name in self._DTO_members,'name not in _DTO_members',name=name,members=self._DTO_members)
        self._DTO_members = [x for x in self._DTO_members if x != name]
        
    def DTO_add_field(self,name,value):
        self._add_DTO_member(name)
        setattr(self,name,value)
        return self

    def DTO_remove_field(self,name,field_names=None):
        if field_names is None:
            field_names = [name]
        for fname in field_names:
            delattr(self,fname)
        self._remove_DTO_member(name)
        return self
        
    def _to_dct(self):
        return dict(self.itermembers())
    
    def itermembers(self):
        return ((k, getattr(self, k)) for k in self._DTO_members)
        
    def __str__(self):
        contents = ['%s=%s' % (k,getattr(self,k)) for k in self._DTO_members]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(contents))    

    def __repr__(self):
        contents = ['%s=%r' % (k,getattr(self,k)) for k in self._DTO_members]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(contents))    

    def __cmp__(self,other):
        if type(self) != type(other):
            return cmp(type(self).__name__, type(other).__name__)
        if self._DTO_members != other._DTO_members:
            return cmp(self._DTO_members, other._DTO_members)
        for k in self._DTO_members:
            x = cmp(getattr(self,k),getattr(other,k))
            if x != 0:
                return x
        return 0

    def _eq_with_diff(self, other, logger=None):
        if type(self).__name__ != type(other).__name__:
            if logger is not None:
                logger.Debug('DTO.__eq__ - types are different type(self)=%s, type(other)=%s' % (type(self),type(other)))
            return False
        if self._DTO_members != other._DTO_members:
            if logger is not None:
                logger.Debug('DTO.__eq__ - members are different self=%s, other=%s' % (self._DTO_members,other._DTO_members))
            return False
        for k in self._DTO_members:
            self_k = getattr(self,k)
            other_k = getattr(other,k)
            if self_k != other_k:
                if logger is not None:
                    logger.Debug('DTO.__eq__ - member %s is different. self=%s, other=%s' % (k,self_k,other_k))
                return False
        return True

    def __eq__(self,other):
        """Provide __eq__ and __ne__ when members don't support cmp (e.g, for sets)"""
        return self._eq_with_diff(other)

    def __ne__(self,other):
        return not self.__eq__(other)

    def __hash__(self):
        res = 0
        for k in self._DTO_members:
            val = getattr(self,k)
            try:
                res = res ^ hash(val)
            except:
                pass # ignore members which aren't hashable
        return res

#####################################
# Bunch
#####################################

class Bunch(DTO):
    _code_version = 0
    def __init__(self,**kw):
        kw['self'] = self
        super(Bunch,self).__init__(kw)

class BunchKw(DTO):
    _code_version = 0
    def __init__(self,kw):
        kw['self'] = self
        super(BunchKw,self).__init__(kw)

#####################################
# Anything
#####################################

class Anything(object):
    """Provides an object x which you can hang arbitrary data on:
       x.y = my_data
       x.z = some_other_data
    """
    def __init__(self,**kw):
        for k,v in kw.iteritems():
            setattr(self,k,v)

    def __repr__(self):        
        return 'Anything(%s)' % ', '.join('%s=%s' % (k,v) for k,v in self.__dict__.iteritems())

    def __eq__(self,other):
        """Provide __eq__ and __ne__ when members don't support cmp (e.g, for sets)"""
        return self.__dict__ == other.__dict__
