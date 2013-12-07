from test_infra_base import BackendInfraTest
from null_object import NullObject

class TestNullObject(BackendInfraTest):
    def test_normal(self):
        null = NullObject()
        other_null = NullObject()
        self.assertEqual(id(null),id(other_null))
        self.assertEqual(repr(null),'NullObject()')
        self.failIf(null)
        self.assertEqual(null(3,x=4),null)
        self.assertEqual(null.x,null)        
        null.y = 3
        del null.z
        self.assertEqual(len(null),0)
        self.assertEqual(list(null),[])
        self.assertEqual(null['x'],null)
        null[3] = 'abc'
        del null[0]        

from unit import build_suite, run_suite
def suite():    
    return build_suite(TestNullObject)

if __name__ == '__main__':
    run_suite(suite())
