import inspect
from types import ModuleType, ClassType, FunctionType

def indent(lst):
    new_lst = []
    for x in lst:
        new_lst.append("\t%s" % x)
    return new_lst

class DummyPackager():

    def __init__(self, package):

        with open(package.__name__ + '.py', 'w') as f:
            f.write('\n'.join(self.__export(package)))

    def __export(self, parent, class_=None):
        buf = []
        lst = dir(parent)
        for x in lst:
            val = getattr(parent, x)
            if x.startswith('__'):
                pass
            elif isinstance(val, int) \
                or isinstance(val, float):
                buf.append('%s=%d' % (x, val))
            elif type(val) == str:
                buf.append('%s="%s"' % (x, val))
            elif inspect.ismodule(val):
                pass
            elif isinstance(val, property):
                if val.fget:
                    buf.append('@property')
                    buf.append('def %s(self): pass'  % (x))
                if val.fset:
                    buf.append('@property')
                    buf.append('def %s(self, v): pass'  % (x))
            elif inspect.isclass(val):
                buf.append('class %s():' % val.__name__)
                buf += indent(self.__export(val, class_=val))
            elif inspect.isfunction(val):
                buf.append('def %s(*args, **kwargs): pass'  % (val.func_name))
            elif isinstance(val, staticmethod):
                buf.append('@staticmethod')
                buf.append('def %s(*args, **kwargs): pass'  % (val.func_name))
            elif isinstance(val, classmethod):
                buf.append('@classmethod')
                buf.append('def %s(cls, *args, **kwargs): pass'  % (val.func_name))
            elif inspect.isfunction(val):
                buf.append('def %s(*args, **kwargs): pass' % (val.func_name))
            elif inspect.ismethod(val):
                buf.append('def %s(self, *args, **kwargs): pass' % (val.func_name))
            elif 'Boost.Python.function' in str(type(val)): # like staticmethod
                if class_:
                    buf.append('@staticmethod')
                buf.append('def %s(*args, **kwargs): pass' % (val.__name__))
            else:
                print 'NOT available type=%s, %s, %s' % (type(val), x, dir(x))

        return buf