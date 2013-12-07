import logging
from pprint import pformat
LOG_FILENAME = 'example.log'
logging.basicConfig(filename=LOG_FILENAME,level=logging.INFO)
vmx_file = 'Ubuntu10_WANBridge.vmx'

#input = open(vmx_file, 'r')
#output = open('out.vmx', 'w')
data = []
with open(vmx_file, 'r') as input:
	with open('out.vmx', 'w') as output:
		for line in input:
			data.append(line.replace('\n',''))
		logging.info(pformat(data))