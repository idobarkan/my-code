class DynamicProxy(object):
    '''Mixin class that acts similarly to Java's dynamic proxy:
       If Class A inherits from DynamicProxy then whenever a method
       is called on class A (with an attribute that A doesn't possess), then
       method _dispatch(method_name,*a,**kw) is called instead.
       The subclass can override _is_callable. Returning False for an attribute causes
       _get_property(attribute_name) to be called instead of waiting for call completion and calling _dispatch.
    '''
    def __getattr__(self,name):
        if self._is_callable(name):        
            return DynamicProxy.CalledNameHelper(self,name)
        else:            
            return self._get_property(name)

    def _is_callable(self,
                     name): #@UnusedVariable
        """Override this method in subclass to define attributes that are properties and not methods"""
        return True

    class CalledNameHelper(object):
        def __init__(self, proxy, method_name):
            self.proxy = proxy
            self.method_name = method_name
            self.__name__ = self.method_name
            # Take additional params from the method
            self.__dict__.update(self.proxy._dispatch.__dict__)
            
        def __repr__(self):
            return 'CalledNameHelper(proxy=%s,method_name=%s)' % (self.proxy,self.method_name)
        
        def __call__(self, *a, **kw):
            return self.proxy._dispatch(self.method_name, *a, **kw)
        
