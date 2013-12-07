import logging
import pprint
from pprint import pformat

LOG_FILENAME = 'example.log'
logging.basicConfig(filename=LOG_FILENAME,level=logging.INFO)
	
stuff = ['spam', [('eggs', ("'spam' and\n eggs",),),'spam']]

logging.info('Logging pformatted data')
logging.info(pformat(stuff))





#logging.info('This message should go to the log file')