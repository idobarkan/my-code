import re

class ValidationException(Exception):
    pass

def validate_ip_string(ip,b_allow_none=False):
    def error(msg):
        raise ValidationException('Invalid IP %s: %s' % (ip,msg))

    if ip is None:
        if b_allow_none: return 
        else: error('None not allowed')

    if not isinstance(ip, str):
        error('IP must be a string') 

    exp = re.compile(r'^[\d\.]+$')  # from beginning to end: only dots or digits      
    if not (re.search(exp, ip)): 
        error('IP should contain integers and dots alone')

    try:
        parts = [int(p) for p in ip.split('.')]
    except:
        error('IP should be composed of integers separated by dots')
    if len(parts) != 4: error('IP should have 4 parts')
    for i,p in enumerate(parts):
        if not (0 <= p <= 255): error("parts should be 8 bit numbers")
        if i==0 and p==0: error("first part can't be 0")


def validate_subnet_and_mask(subnet,n_bits,b_allow_none):
    def error(msg):
        raise ValidationException('Invalid subnet/netmask combination %s/%s: %s' % (subnet,n_bits,msg))

    if not (1 <= n_bits <= 32): error('number of subnet bits must be between 1 and 32')
    int_subnet = _get_ip_bits(subnet,b_allow_none)
    mask_out = (1<<(32-n_bits)) - 1            
    if int_subnet & mask_out != 0: error("subnet contains non zero bits outside mask")

def validate_ip_in_subnet(ip,subnet,n_bits,b_allow_none=False):
    if ip is None:
        if b_allow_none: return 
        else: raise ValidationException('None not allowed')

    subnet_bits = _get_ip_bits(subnet)
    ip_bits = _get_ip_bits(ip)
    subnet_bits_of_subnet = subnet_bits>>(32-n_bits)
    subnet_bits_of_ip = ip_bits>>(32-n_bits)
    if not subnet_bits_of_subnet==subnet_bits_of_ip:
        raise ValidationException('Invalid subnet/ip combination: subnet=%s, ip=%s, n_bits=%s' % (subnet,ip,n_bits))
    
def _get_ip_bits(ip_string,b_allow_none=False):
    validate_ip_string(ip_string,b_allow_none=b_allow_none)
    int_ip = 0
    for p in ip_string.split('.'):
        int_ip = int_ip*256 + int(p)
    return int_ip
    
def validate_mac_string(mac,b_allow_none=False):
    def error(msg):
        raise ValidationException('Invalid MAC %s: %s' % (mac,msg))

    if mac is None:
        if b_allow_none: return 
        else: error('None not allowed')

    if not isinstance(mac, str):
        error('MAC must be a string') 
    try:
        parts = [int(p,16) for p in mac.split(':')]
    except:
        error('MAC should be composed of hex separated by colons')
    if len(parts) != 6: error('MAC should have 6 parts')
    for p in parts:
        if not (0 <= p <= 255): error("parts should be 8 bit numbers")