from test_infra_base import BackendInfraTest
from infra.util import fmt_exc

from infra import validations

class TestValidations(BackendInfraTest):
    def _validate(self,f,a,kw,expected_warning):
        try:
            f(*a,**kw)
        except validations.ValidationException, e:
            self.assert_(expected_warning,"Unexpected exception: %s" % fmt_exc(e,b_short=True))
            self.assert_(expected_warning in e.message,"Expected message to contain: %s. Got message: %s" % (expected_warning,e.message))
        else:
            self.assert_(not expected_warning,"Did not get expected exception: %s" % (expected_warning,))

    def test_ip(self):
        def validate(ip,expected_warning=None,**kw):
            self._validate(validations.validate_ip_string,(ip,),kw,expected_warning)

        validate('192..1.2', expected_warning = 'IP should be composed of integers separated by dots')
        validate(' 192.168.1.2', expected_warning = 'IP should contain integers and dots alone')
        validate('192.  168.1.2', expected_warning = 'IP should contain integers and dots alone')
        validate('192.168.1.0')    
        validate(None,expected_warning = 'None not allowed')
        validate(None,b_allow_none=True)
        validate('192.168.1',expected_warning = 'IP should have 4 parts')
        validate('192.168.x',expected_warning = 'IP should contain integers and dots alone')
        validate(3,expected_warning = 'IP must be a string')
        validate('192.168.1.256',expected_warning = 'parts should be 8 bit numbers')
        validate('1.0.0.0')
        validate('0.1.1.1',expected_warning = "first part can't be 0")

    def test_mac(self):
        def validate(mac,expected_warning=None,**kw):
            self._validate(validations.validate_mac_string,(mac,),kw,expected_warning)

        validate('00::11:22:33:44', expected_warning = 'MAC should be composed of hex separated by colons')
        validate(None,expected_warning = 'None not allowed')
        validate(None,b_allow_none=True)
        validate('00:11:22:33:44',expected_warning = 'MAC should have 6 parts')
        validate('00:11:22:33:44:x',expected_warning = 'MAC should be composed of hex separated by colons')
        validate(3,expected_warning = 'MAC must be a string')
        validate('00:11:22:33:44:100',expected_warning = 'parts should be 8 bit numbers')
        

    def test_subnet_and_mask(self):
        def validate(subnet,n_bits,expected_warning=None):
            self._validate(validations.validate_subnet_and_mask,(subnet,n_bits,True),{},expected_warning)
                
        validate('192.168.1.0',24)
        validate('192.168.1.0',23,expected_warning='Invalid subnet/netmask combination 192.168.1.0/23: subnet contains non zero bits outside mask')
        validate('192.168.asdf.3',24,expected_warning='Invalid IP 192.168.asdf.3: IP should contain integers and dots alone')
        validate('192.168.1',24,expected_warning='Invalid IP 192.168.1: IP should have 4 parts')
        validate('192.168.7.0',23,expected_warning='Invalid subnet/netmask combination 192.168.7.0/23: subnet contains non zero bits outside mask')
        validate('192.168.6.0',23)
        validate('192.168.6.1',32)
        validate('192.168.6.2',31)
        validate('192.168.6.3',31,expected_warning='Invalid subnet/netmask combination 192.168.6.3/31: subnet contains non zero bits outside mask')

    def test_validate_ip_in_subnet(self):
        def validate(ip,subnet,n_bits,expected_warning=None):
            self._validate(validations.validate_ip_in_subnet,(ip,subnet,n_bits),{},expected_warning)
        
        validate('192.168.1.0','192.168.1.0',24)
        validate('192.168.1.3','192.168.1.0',24)
        validate('192.168.3.3','192.168.1.0',24,expected_warning='Invalid subnet/ip combination')
        validate('8.168.3.3','192.168.1.0',24,expected_warning='Invalid subnet/ip combination')

from infra.unit import build_suite, run_suite
def suite():    
    return build_suite(TestValidations)

if __name__ == '__main__':
    run_suite(suite())
