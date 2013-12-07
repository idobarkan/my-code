import unittest
import add_parent_path # PyFlakesIgnore

from reset_state import reset_state

class TestResetState(unittest.TestCase):
    def test_sanity(self):
        @reset_state
        class A(object):
            def __init__(self,x,y):
                self.set_xy(x,y)
            def set_xy(self,x,y):
                self.x = x
                self.y = y

        def verify(a,x,y):
            self.assertEqual(a.x,x)
            self.assertEqual(a.y,y)
                
        a = A(1,'ronnie')
        verify(a,1,'ronnie')

        a.set_xy(3,10)
        verify(a,3,10)
        
        a.reset_state()
        verify(a,1,'ronnie')
        
        # verify another instance doesn't interfere with original
        a2 = A(2,'michal')
        verify(a2,2,'michal')
        a.set_xy(6,6)
        a2.set_xy(11,11)
        a2.reset_state()
        verify(a2,2,'michal')
        verify(a,6,6)
                
if __name__ == '__main__':
    unittest.main()
