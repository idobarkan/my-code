import exceptions

class EnumException(exceptions.Exception):
    pass

class EnumItem(object):
    def __init__(self,enum_name,val,name):
        self.enum_name = enum_name
        self.val = val
        self.name = name
        
    @property # for compatibility with C# enums during transition to CPython
    def value__(self): return self.val
        
    def __hash__(self):
        return hash(self.val) ^ hash(self.name)
    def __cmp__(self,other):
        if not isinstance(other,EnumItem):
            return 1
        if self.enum_name != other.enum_name:
            return cmp(self.enum_name,other.enum_name)
        return cmp(self.val,other.val)
    def __str__(self):
        return self.name
    def __repr__(self):
        return 'item(%s,%s)' % (self.name,self.val)

class Enum(object):
    """*@DynamicAttrs*"""
    def __init__(self, enum_name, enumList):
        self.enum_name = enum_name
        self.lookup = []
        self.reverseLookup = {}
        for name in enumList:
            if type(name) == tuple:
                name, val = name
            else:
                val = None
            self.add_item(name,val)

    def add_item(self,name,val=None):
        if val is None:
            val = max(self.reverseLookup.iterkeys()) + 1 if self.reverseLookup else 0
        self._checkEntry(name,val)
        self.lookup.append(name)
        self.reverseLookup[val] = name
        setattr(self, name, EnumItem(self.enum_name,val,name))
        return getattr(self, name)
            
    def _checkEntry(self,name,val):
        if type(name) != str:
            raise EnumException, "enum name is not a string: %s" % (name,)
        if type(val) != int:
            raise EnumException, "enum value is not an integer: %s" % (val,)
        if name in self.__dict__:
            raise EnumException, "enum name is not unique: %s" % (name,)
        if val in self.reverseLookup:
            raise EnumException, "enum value is not unique for %s" % (name,)

    def get_by_value(self,val):
        name = self.reverseLookup[val]
        return getattr(self, name)
    
    def get_by_name(self, name):
        return getattr(self, name)
        
    def items(self):
        lst_items = [getattr(self, name) for name in self.lookup]
        sorted_items = sorted(lst_items,key=lambda x:x.val)
        return sorted_items
        
    def is_legal_value(self,x):
        for item in self.items():
            if x == item:
                return True
        return False
        
