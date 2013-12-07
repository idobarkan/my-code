from test_infra_base import BackendInfraTest
import assertions
from util import fmt_exc
from mock_object.mock import Mock
import itertools

class TestAssertions(BackendInfraTest):
    def setUp(self):
        super(TestAssertions,self).setUp()
        assertions.Assertions.TEST_reset_config()
        assertions.Assertions.reset_events()
        self.alert_sender = Mock()
        self.alert_sender.return_value = None
        self.mock_logger = object()
        assertions.Assertions.alert_sender = self.alert_sender
        assertions.Assertions.logger = self.mock_logger
    
    def test_fail(self):
        self.assertRaises(assertions.AssertionException,assertions.fail,'some message')
        self.assertEquals(assertions.Assertions.had_assertion,True)
        self.alert_sender.assert_called_with(self.mock_logger, assertions.MsgType.Assertion, 'some message')            
        
        # verify we get the details of the error in the exception
        try:
            assertions.fail('problem', x=666, error=fmt_exc(AttributeError('blabla')))
        except assertions.AssertionException, e:
            error_msg = e.Message            
        else:
            self.fail('did not get exception as expected')
        self.assert_('problem' in error_msg, error_msg)
        self.assert_('666' in error_msg, error_msg)
        self.assert_('AttributeError' in error_msg, error_msg)
        self.assert_('blabla' in error_msg, error_msg)
        
    def test_fail_with_lambda(self):
        try:
            z = 777
            assertions.fail(lambda: 'fail' + str(z), x=666)
        except assertions.AssertionException, e:
            error_msg = e.Message            
        else:
            self.fail('did not get exception as expected')
        self.assert_('fail777' in error_msg, error_msg)
        self.assert_('666' in error_msg, error_msg)
        
    def test_conditional_with_lambda(self):
        try:
            z = 777
            def foo():
                z = 888
                return 'assertionfailed' + str(z)
            
            assertions.assert_that(z == 777, foo)
            assertions.assert_that(z != 777, foo)
        except assertions.AssertionException, e:
            error_msg = e.Message            
        else:
            self.fail('did not get exception as expected')
        self.assert_('assertionfailed888' in error_msg, error_msg)

    def test_fail_with_sender_formatting(self):
        formatted_msg = 'my formatted message'
        self.alert_sender.return_value = formatted_msg
        
        # verify we get the details of the error in the exception
        try:
            assertions.fail('some message')
        except assertions.AssertionException, e:
            error_msg = e.Message            
        else:
            self.fail('did not get exception as expected')
        
        self.assertEquals(error_msg,formatted_msg)
        
    def test_warn(self):
        assertions.warn('problem',name='john')
        self.assertEquals(assertions.Assertions.had_assertion,True)
        self.alert_sender.assert_called_with(self.mock_logger, assertions.MsgType.Warning, 'problem', name='john')

    def test_conditional(self):
        for base,variant,meet_condition in itertools.product(['fail','warn'],['if','unless'],[True,False]):
            self.alert_sender.reset()
            fname = base + '_' + variant
            f = getattr(assertions, fname)
            
            if variant == 'if':
                cond_param = meet_condition
            else:
                cond_param = not meet_condition
            
            # run the method
            had_test_exception = False
            try:
                f(cond_param,'it failed', x=3,name='jane')
            except assertions.AssertionException:
                had_test_exception = True
                
            # check result
            which_test = 'base=%s, variant=%s, do_fail=%s' % (base,variant,meet_condition)
            if meet_condition: # assertion/warning triggered
                if base == 'fail':
                    self.assert_(had_test_exception,which_test)
                if base == 'fail':
                    header = assertions.MsgType.Assertion
                else:
                    header = assertions.MsgType.Warning
                self.assertEquals(assertions.Assertions.had_assertion,True)
                self.alert_sender.assert_called_with(self.mock_logger, header, 'it failed', x=3, name='jane')
            else:
                self.failIf(self.alert_sender.called,'assertion/warning should not have happened. %s' % which_test)

    def test_change_logger(self):
        other_logger = object()
        x = 5
        assertions.warn_if(x>3, 'problem', x=x, logger=other_logger)
        self.alert_sender.assert_called_with(other_logger, assertions.MsgType.Warning, 'problem', x=5)
        

class TestDefaultSender(BackendInfraTest):
    def setUp(self):
        super(TestDefaultSender,self).setUp()
        assertions.Assertions.TEST_reset_config()
        assertions.Assertions.reset_events()
        self.mock_logger = Mock()
        assertions.Assertions.logger = self.mock_logger
    
    def test_basic_formatting(self):
        assertions.warn('problem',name='john')
        self.mock_logger.Warn.assert_called_with('problem. name=john')
        self.assertRaises(assertions.AssertionException, assertions.fail, 'another problem', name='jane')
        self.mock_logger.Error.assert_called_with('another problem. name=jane')
        
    def test_formatting_error(self):
        class BadStr(object):
            def __repr__(self):
                raise Exception,"can't format this object to string"

        assertions.warn('a problem', bad=BadStr())
        self.mock_logger.Warn.assert_called_with('ASSERTION. NO INFO - ERROR WHILE FORMATTING ARGS!')
        
                   
from unit import build_suite, run_suite, combine_suites
def suite():
    return combine_suites(
        build_suite(TestAssertions), 
        build_suite(TestDefaultSender),
    )
    
if __name__ == '__main__':
    run_suite(suite())
