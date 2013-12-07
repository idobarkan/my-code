from util import dotnet_import
clr = dotnet_import("clr")
if clr is not None:
    import System
    clr.AddReference('IronPython')
    import IronPython
    clr.AddReference('Microsoft.Scripting')
    from Microsoft.Scripting.Hosting import ExceptionOperations
    
import assertions
import traceback
import sys

def convert_exceptions(mapping):
    """Function that returns a method decorator. 
       The decorator converts any exceptions according to the given mapping.
       mapping is a dictionary from original exception types to target exception types.
       If an exception is thrown that doesn't match any of the mapped types, it is re-raised as is.
       Note that if a convertion is performed, the original stack trace is lost.
    """
    def decorator(f):
        def _wrapped(*a,**kw):
            try:
                return f(*a,**kw)
            except Exception, e:
                for src,target in mapping.iteritems():
                    if isinstance(e,src):
                        raise target(str(e))
                raise
        _wrapped.__name__ = f.__name__
        return _wrapped
    return decorator    

# create a python engine for formatting exceptions
if clr is not None:
    exception_operations = IronPython.Hosting.Python.CreateRuntime().GetEngine("py").GetService[ExceptionOperations]()   
    assertions.fail_if(exception_operations is None, "Exception operations was not loaded properly, check assembly for IronPython DLL version")
else:
    exception_operation = None

def set_current_traceback():
    """ Set the current traceback on the current exception, so it will printed when the exception is formatted
        Good for using with context manager, to get the "interesting" stack trace.
    """
    _, exc, tb = sys.exc_info()
    exc.inner_tb = tb

def fmt_exc(exc, b_short=False, b_message_only=False, exc_traceback=None):
    """Needs to handle 8 cases:
       * original exception is python or C#
       * exception constructed or caught (as python Exception)
       * b_short True or False
       * tb - traceback object to get the trace from (instead of the exception)
    """
    try:
        cls_exc = _get_cls_exception(exc)
        if cls_exc is None:
            typename, msg, trace, inner = _get_python_exc_details(exc, exc_traceback)
        else:
            typename, msg, trace, inner = _get_cls_exc_details(cls_exc)
        print "@@@Ido .fmt_exc- trace={trace}".format(**locals())
        if b_message_only:
            return str(msg)
        str_result = 'exception_type=%s, msg=%s' % (typename,msg)
        if not b_short and trace is not None:
            str_result += '. Stack:\n' + trace
            if inner is not None:
                str_result += '\r\nINNER EXCEPTION: ' + fmt_exc(inner)
        return str_result
    except Exception as e:
        try:
            try:
                return 'ERROR WHILE FORMATTING EXCEPTION: e=' + fmt_exc(e, exc_traceback=sys.exc_info()[2]) + ", exc=" + str(exc)
            except Exception:
                return 'ERROR WHILE FORMATTING EXCEPTION: e=' + str(e) + ", exc=" + str(exc)
        except Exception:
            return 'ERROR WHILE FORMATTING EXCEPTION. Cant even show the error while formatting!'


def _get_cls_exception(exc):
    if clr is None:
        return None
    if isinstance(exc, System.Exception):
        return exc
    if not hasattr(exc, 'clsException'):
        return None

    # it's a python exception having a clsException attribute, meaning it was wrapped by catching it as python exception.
    # the original exception may still be either python or C#
    if exc.__class__.__name__ in ['StandardError','SystemError']: # wrapped errors have C# type of "StandardError" and sometimes 'SystemError'
        return exc.clsException
    else:
        return None

def _extract_trace(cls_exc):
    try:
        long_msg = exception_operations.FormatException(cls_exc)
        trace_lines = long_msg.split('\n')
        exc_trace_lines = []
        for line in trace_lines[1:]:
            if line.lstrip().startswith('File '): 
                exc_trace_lines.append(line)
            else: 
                break
        exc_trace = '\n'.join(exc_trace_lines)
        return exc_trace
    except Exception as e:
        return 'ERROR WHILE FORMATTING STACK TRACE: e=' + str(e)

def _get_cls_exc_details(cls_exc):
    typename = type(cls_exc).__name__
    msg = cls_exc.Message    
    trace = _extract_trace(cls_exc)
    inner = cls_exc.InnerException
    return (typename, msg, trace,inner)

def _get_python_exc_details(exc, exc_traceback=None):
    typename = exc.__class__.__name__
    msg = str(exc)
    if clr is not None:
        cls_exc = getattr(exc, 'clsException', None)
        if cls_exc is None:
            trace = None
        else:
            trace = _extract_trace(cls_exc)
    else:
        if exc_traceback:
            print "@@@Ido ._get_python_exc_details- exc_traceback".format(**locals())
            trace = "".join(traceback.format_list(traceback.extract_tb(exc_traceback)))
        elif hasattr(exc, 'trace'):
            print "@@@Ido ._get_python_exc_details- hasattr(exc, 'trace')".format(**locals())
            trace = exc.trace
        else:
            print "@@@Ido ._get_python_exc_details- else".format(**locals())
            trace = str(exc)
        
    if hasattr(exc, 'inner_tb'):
        trace += 'INNER TRACEBACK:\n' + ''.join(traceback.format_tb(exc.inner_tb))
    inner = None
    return (typename, msg, trace, inner)
