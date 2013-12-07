from test_infra_base import BackendInfraTest
from dynamic_proxy import DynamicProxy

class TestDynamicProxy(BackendInfraTest):
    def test_normal(self):
        class MyProxy(DynamicProxy):
            def __init__(self,x):
                DynamicProxy.__init__(self)
                self.x = x
            def _dispatch(self,method_name,*a,**kw):
                return 'x=%s, method_name=%s, a=%s, kw=%s' % (self.x,method_name,a,kw)

        p = MyProxy(666)
        s = p.foo(1,True,y='Jim')
        self.assertEqual(s,"x=666, method_name=foo, a=(1, True), kw={'y': 'Jim'}")

    def test_property(self):
        class MyProxy(DynamicProxy):
            def __init__(self):
                DynamicProxy.__init__(self)

            def _is_callable(self,name):
                return name == 'mth'

            def _dispatch(self,method_name):
                return method_name

            def _get_property(self,name):
                return name

        p = MyProxy()
        self.assertEqual(p.prop,'prop')
        self.assertEqual(p.mth(),'mth')
    
    def test_method_attributes(self):
        def set_something(f):
            f.something = 3
            return f
        
        class MyProxy(DynamicProxy):
            def __init__(self):
                DynamicProxy.__init__(self)
                
            @set_something
            def _dispatch(self,method_name,*a,**kw):
                pass
            
        p = MyProxy()
        foo = p.foo
        self.assertEqual(foo.__name__,'foo')
        self.assertEqual(foo.something,3)
        
from unit import build_suite, run_suite
def suite():    
    return build_suite(TestDynamicProxy)

if __name__ == '__main__':
    run_suite(suite())
