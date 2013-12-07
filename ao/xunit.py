"""This plugin provides test results in the standard XUnit XML format.

It was designed for the `Hudson`_ continuous build system but will 
probably work for anything else that understands an XUnit-formatted XML
representation of test results.

Add this shell command to your builder ::
    
    nosetests --with-xunit

And by default a file named nosetests.xml will be written to the 
working directory.  

In a Hudson builder, tick the box named "Publish JUnit test result report"
under the Post-build Actions and enter this value for Test report XMLs::
    
    **/nosetests.xml

If you need to change the name or location of the file, you can set the 
``--xunit-file`` option.

Here is an abbreviated version of what an XML test report might look like::
    
    <?xml version="1.0" encoding="UTF-8"?>
    <testsuite name="nosetests" tests="1" errors="1" failures="0" skip="0">
        <testcase classname="path_to_test_suite.TestSomething" 
                  name="path_to_test_suite.TestSomething.test_it" time="0">
            <error type="exceptions.TypeError">
            Traceback (most recent call last):
            ...            
            TypeError: oops, wrong type
            </error>
        </testcase>
    </testsuite>

.. _Hudson: https://hudson.dev.java.net/

"""

import traceback
import inspect
from time import time

def xmlsafe(s, encoding="utf-8"):
    """Used internally to escape XML."""
    if isinstance(s, unicode):
        s = s.encode(encoding)
    s = str(s)
    for src, rep in [('&', '&amp;', ),
                     ('<', '&lt;', ),
                     ('>', '&gt;', ),
                     ('"', '&quot;', ),
                     ("'", '&quot;', ),
                     ]:
        s = s.replace(src, rep)
    return s

def nice_classname(obj):
    """Returns a nice name for class object or class instance.
    
        >>> nice_classname(Exception()) # doctest: +ELLIPSIS
        '...Exception'
        >>> nice_classname(Exception)
        'exceptions.Exception'
    
    """
    if inspect.isclass(obj):
        cls_name = obj.__name__
    else:
        cls_name = obj.__class__.__name__
    mod = inspect.getmodule(obj)
    if mod:
        name = mod.__name__
        # jython
        if name.startswith('org.python.core.'):
            name = name[len('org.python.core.'):]
        return "%s.%s" % (name, cls_name)
    else:
        return cls_name

class Xunit(object):
    """This plugin provides test results in the standard XUnit XML format."""
    name = 'xunit'
    score = 2000
    encoding = 'UTF-8'
    def __init__(self, xunit_file):
        self.stats = {'errors': 0,
                      'failures': 0,
                      'passes': 0,
                      'skipped': 0
                      }
        self.testlist = []
        self.xunit_file = xunit_file
        
    def _xmlsafe(self, s):
        return xmlsafe(s, encoding=self.encoding)
    
    def _exc_info_to_string(self, 
                            err, 
                            test): #@UnusedVariable
        return ''.join(traceback.format_exception(*err))
    
    def report(self):
        """Writes an Xunit-formatted XML file

        The file includes a report of test errors and failures.

        """
        self.stats['encoding'] = self.encoding
        self.stats['total'] = (self.stats['errors'] + self.stats['failures']
                               + self.stats['passes'] + self.stats['skipped'])
        self.error_report_file = open(self.xunit_file, 'w')
        self.error_report_file.write(
            '<?xml version="1.0" encoding="%(encoding)s"?>\n'
            '<testsuite name="unittests" tests="%(total)d" '
            'errors="%(errors)d" failures="%(failures)d" '
            'skip="%(skipped)d">\n' % self.stats)
        self.error_report_file.write('\n'.join(self.testlist))
        self.error_report_file.write('\n</testsuite>')
        self.error_report_file.close()

    def startTest(self,
                  test): #@UnusedVariable
        """Initializes a timer before starting a test."""
        self._timer = time()
        self.errors = []
       
    def addError(self, 
                 test, 
                 err, 
                 capt=None): #@UnusedVariable
        """Add error output to Xunit report.
        """        
        self.errors.append('ERROR\n'+'='*70+'\n'+self._xmlsafe(self._exc_info_to_string(err, test)))

    def addFailure(self, 
                   test, 
                   err, 
                   capt=None, #@UnusedVariable
                   tb_info=None): #@UnusedVariable
        """Add failure output to Xunit report.
        """
        self.errors.append('FAILURE\n'+'='*70+'\n'+self._xmlsafe(self._exc_info_to_string(err, test)))
        
    def addSuccess(self, test, capt=None):
        """Add success output to Xunit report.
        """
        pass
        
    def stopTest(self, test):
        taken = time() - self._timer
        test_id = '.'.join(test.id().split('.')[-3:])
        if self.errors:
            self.stats['failures'] += 1
            str_errors = '<error>\n' + '\n'.join(self.errors) + '\n</error>\n'
        else: 
            self.stats['passes'] += 1
            str_errors = ''
        self.testlist.append(
            '<testcase classname="%(cls)s" name="%(name)s" time="%(taken)d">\n%(str_errors)s</testcase>' %
            {'cls': self._xmlsafe('.'.join(test_id.split('.')[:-1])),
             'name': self._xmlsafe(test_id),
             'taken': taken,
             'str_errors': str_errors,
             })