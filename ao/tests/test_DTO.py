from test_infra_base import BackendInfraTest
import pickle

from DTO import DTO, Bunch, BunchKw, Anything

class TestDTO(BackendInfraTest):
    def test_normal(self):
        class A(DTO):
            def __init__(self,i,j):
                super(A,self).__init__(locals())
                k = 3 # check this doesn't appear in locals() @UnusedVariable
            @property
            def j(self): return -self._j
            @j.setter
            def j(self,val): self._j = -val 
                
        a = A(3,5)
        self.assertEqual(str(a),'A(i=3, j=5)')
        self.assertEqual(a.i,3)
        self.assertEqual(a.j,5)
        self.assertEqual(a._j,-5)
        b = A(3,5)
        c = A(2,4)
        self.assertEqual(a,b)
        self.assertNotEqual(a,c)
        self.assert_(a>c,'a=%s, c=%s' % (a,c))
        self.assertNotEqual(a,None)

    def test_hash(self):
        class A(DTO):
            def __init__(self,i,j):
                super(A,self).__init__(locals())
        lst = [A(3,'abc'),A(3,3),A(True,4.5)]
        hash_set = set(hash(x) for x in lst)
        self.assertEqual(len(hash_set),len(lst))
        for a in lst:
            other = A(a.i,a.j)
            self.assertEqual(a,other)
            self.assertEqual(hash(a),hash(other))

    def test_eq(self):
        class A(DTO):
            def __init__(self,i,j):
                super(A,self).__init__(locals())
        a = A(set([1,2,3]),True) 
        b = A(set([1,2,3]),True)
        c = A(set([1,2]),True)
        def greater(x,y):
            return x>y
        self.assertRaises(TypeError,greater,a,c) # sets are not comparable using cmp        
        self.assertEqual(a==b,True)
        self.assertEqual(a!=b,False)
        self.assertEqual(a==c,False)
        self.assertEqual(a!=c,True)
        
    def test_to_dct(self):
        class A(DTO):
            def __init__(self,i,j):
                super(A,self).__init__(locals())
        a = A(i=3, j='xyz')
        self.assertEqual(a._to_dct(), {'i':3, 'j':'xyz'})

    def test_itermembers(self):
        class A(DTO):
            def __init__(self,i,j):
                super(A,self).__init__(locals())
        a = A(i=3, j='xyz')
        dict(a.itermembers())
        self.assertEqual(dict(a.itermembers()),a._to_dct())
        
    def test_change_fields(self):
        class A(DTO):
            def __init__(self,i,j):
                super(A,self).__init__(locals())
        a = A(i=3,j=5)
        self.assertRaises(TypeError, A, i=3,j=5,k=8)
        
        a.DTO_add_field('k',8)
        self.assertEqual(a.k,8)
        self.assertEqual(a._to_dct(), {'i':3, 'j':5, 'k':8})
        
        a.DTO_remove_field('j')
        self.assertRaises(AttributeError,getattr,a,'j')
        self.assertEqual(a._to_dct(), {'i':3, 'k':8})

        # check use when one of the members is a property
        class B(DTO):
            def __init__(self,x,y):
                super(B,self).__init__(locals())
            
            @property
            def x(self): return self._x
            @x.setter
            def x(self,x): #PyFlakesIgnore
                self._x = x
                self._x2 = x+1

        b = B(8,0)
        self.assertEqual(b._to_dct(), {'x':8,'y':0})
        self.assert_('_x' in vars(b))
        self.assert_('_x2' in vars(b))
        
        b.DTO_remove_field('x',field_names=['_x','_x2'])
        self.assertEqual(b._to_dct(), {'y':0})
        self.assert_('_x' not in vars(b))
        self.assert_('_x2' not in vars(b))
        
    def test_upgrade(self):    
        # Create object of old class and pickle it
        class A(DTO):
            _code_version = 1
            def __init__(self,i):
                super(A,self).__init__(locals())
        OldA = A

        globals()['A'] = OldA # so pickle can find it
        a = A(3)
        self.assertEqual(type(a),OldA)
        str_dumped = pickle.dumps(a) # NOTE: THIS FAILS WHEN THE TEST IS RUN AS MAIN (can't pickle. class not found as __main__.A). you must the whole infra test.py

        # Unpickle after upgrading to new class
        class A(DTO): #@DuplicatedSignature
            _code_version = 2
            def __init__(self,i,j):
                super(A,self).__init__(locals())
        NewA = A
        globals()['A'] = NewA  # so pickle can find it
        a2 = pickle.loads(str_dumped)

        # verify it's the new class, but with old fields and version
        self.assertEqual(type(a2),NewA)
        self.assertNotEqual(type(a2),OldA)
        self.assertEqual(a2.instance_version,OldA._code_version)
        self.assertEqual(a2.i,a.i)        
        self.failIf(hasattr(a2,'j'))
        
class TestBunch(BackendInfraTest):
    def test_normal(self):
        bunch = Bunch(x=3,y='fred')
        self.assertEqual(str(bunch),"Bunch(x=3, y=fred)")
        self.assertEqual(bunch.x,3)
        self.assertEqual(bunch.y,'fred')

    def test_compare(self):
        b1 = Bunch(x=3,y='fred')
        b2 = Bunch(x=3,y='fred')
        b3 = Bunch(x=4,y='fred')
        b4 = Bunch(x=3,y='fred',z=10)
        b5 = Bunch(j=5)
        self.assertEqual(b1,b2)
        self.assert_(b3>b1)
        self.assertNotEqual(b1,b4)
        self.assertNotEqual(b1,b5)
    
    def test_kw(self):
        dct = {'x':3,'y':'fred','z' : 5}
        bunch = BunchKw(dct)
        self.assertEqual(str(bunch),"BunchKw(x=3, y=fred, z=5)")
        self.assertEqual(bunch.x,3)
        self.assertEqual(bunch.y,'fred')        
        self.assertEqual(bunch.z,5)        

class TestAnything(BackendInfraTest):
    def test_normal(self):
        a = Anything()
        self.assertEqual(str(a),"Anything()")
        a.x = 3
        self.assertEqual(str(a),"Anything(x=3)")
        
        a = Anything(x=3,y='fred')
        self.assert_(str(a) in ["Anything(x=3, y=fred)", "Anything(y=fred, x=3)"], 'str(a)=%s' % str(a))
        self.assertEqual(a.x,3)
        self.assertEqual(a.y,'fred')

    def test_compare(self):
        a1 = Anything(x=3,y='fred')
        a2 = Anything(x=3,y='fred')
        a3 = Anything(x=3,y='fred',z=10)
        a4 = Anything(j=5)
        self.assertEqual(a1,a2)
        self.assertNotEqual(a1,a3)
        self.assertNotEqual(a1,a4)


from unit import build_suite, run_suite, combine_suites
def suite():    
    return combine_suites(
        build_suite(TestDTO),
        build_suite(TestBunch),
        build_suite(TestAnything),
    )

if __name__ == '__main__':
    run_suite(suite())
