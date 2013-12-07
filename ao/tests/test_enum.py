from test_infra_base import BackendInfraTest
from enum import Enum, EnumException

class TestEnum(BackendInfraTest):
    def setUp(self):
        super(TestEnum,self).setUp()
        self.Colors = Enum('Colors',['Red','Green','Blue'])

    def test_get_by_name(self):
        red = self.Colors.Red
        self.assertEqual(red.name,'Red')
        self.assertEqual(red.val,0)
        self.assertEqual(str(red),'Red')

    def test_get_by_value(self):
        red = self.Colors.get_by_value(1)
        self.assertEqual(red.name,'Green')
        self.assertEqual(self.Colors.Blue, self.Colors.get_by_value(2))

    def test_specific_values(self):
        Priority = Enum('Priority',[('Critical',500), ('Medium',250), ('Low',0)])
        med = Priority.Medium
        self.assertEqual(med.val,250)

    def test_lookup_error(self):
        self.assertRaises(AttributeError,getattr, self.Colors,'Purple')
        self.assertRaises(KeyError,self.Colors.get_by_value, 5)

    def test_ctor(self):
        Enum('SomeEnum',[]) # check empty list (should work although not very useful)
        self.assertRaises(EnumException, Enum, 'SomeEnum', ['Yes',5,4])
        self.assertRaises(EnumException, Enum, 'SomeEnum', ['Yes',('No',4),('Maybe','MaybeNot')])
        self.assertRaises(EnumException, Enum, 'SomeEnum', ['Yes','No','Yes']) # duplicate name
        self.assertRaises(EnumException, Enum, 'SomeEnum', ['Yes','No',('Maybe',0)]) # duplicate value

    def test_cmp(self):
        self.assertEqual(self.Colors.Blue,self.Colors.Blue)
        self.assertNotEqual(self.Colors.Blue,self.Colors.Red)
        self.assert_(self.Colors.Red < self.Colors.Blue)

        # comparisons to other types or other enums
        self.assertNotEqual(self.Colors.Red,None)
        Genders = Enum('Genders', ['Male','Female'])
        Genders2 = Enum('Genders2', ['Male','Female','Undecided'])
        self.assertNotEqual(self.Colors.Red,Genders.Male)
        self.assertNotEqual(Genders.Male,Genders2.Male)

    def test_is_legal_value(self):
        self.assertEqual(self.Colors.is_legal_value(self.Colors.Red), True)
        self.assertEqual(self.Colors.is_legal_value(None), False)
        self.assertEqual(self.Colors.is_legal_value(True), False)

    def test_iteration_order(self):
        Fruit = Enum('Fruit',[('Apple',2), ('Orange',0), ('Banana',1)])
        expected_list = [Fruit.Orange,Fruit.Banana,Fruit.Apple]
        self.assertEqual(expected_list,Fruit.items())
        
    def test_add_item(self):
        white = self.Colors.add_item('White')
        self.assertEqual(white, self.Colors.White)
        self.assertEqual(self.Colors.White.val,3)
        self.Colors.add_item('Black',100)
        self.assertEqual(self.Colors.Black.val,100)
        self.assertRaises(EnumException, self.Colors.add_item, 'Red') # duplicate name
        self.assertRaises(EnumException, self.Colors.add_item, 'Purple', 2) # duplicate value

from unit import build_suite, run_suite
def suite():
    return build_suite(TestEnum)

if __name__ == '__main__':
    run_suite(suite())
