"""
Experiment to see what information is present in the stack trace
How do I get the whole traceback (all frames?)

The frames seem to be only recorded from the first point when an exception is
caught

Difficulty is finding the identity of the caller:

https://stackoverflow.com/questions/2203424/python-how-to-retrieve-class-information-from-a-frame-object

"""
import sys
import torch

conv = torch.nn.Conv1d(5, 5, 10)

def b(ace, jar):
    inp = torch.zeros([5, 100])
    return conv(inp)
    # return a(6, {'a', 'b'})

def c(foo, bar):
    return b('abce', [5,3,1])

def d(yab, tab):
    return c(5, 'a')

def e(*args):
    return d({}, 'abc')

OPS = [ torch.nn.modules.conv.Conv1d ]

def get_name(frame):
    code = frame.f_code
    name = code.co_name
    for objname, obj in frame.f_globals.items():
        try:
            assert obj.__dict__[name].__code__ is code
        except Exception:
            pass
        else: # obj is the class that defines our method
            name = '%s.%s' % ( objname, name )
            break
    return name

def get_forward_obj(frame):
    """
    Finds an object with a forward method in the current frame's globals
    and whose class is in a registry of classes
    """
    obj = next((o for o in frame.f_globals.values() if o in OPS), None)
    if obj is None:
        return None
    if obj.forward.__code__ is frame.f_code:
        return obj
    return None

def arg_to_str(val):
    vtype = type(val)
    if isinstance(val, torch.Tensor):
        ten = val
        shape_str = str(list(ten.shape))
        dtype_str = str(ten.dtype).split('.')[1]
        dev_str = ten.device.type
        val = f'{shape_str}:{dtype_str}:{dev_str}'
    elif isinstance(val, (tuple, list, set)):
        val = vtype(arg_to_str(v) for v in val)
    elif isinstance(val, dict):
        val = vtype({arg_to_str(k): arg_to_str(v) for k, v in val.items()})
    else:
        pass
    return val

def print_tensors(exctype, value, tb):
    while tb:
        frame = tb.tb_frame
        obj = get_forward_obj(frame)
        if obj is not None:
            items = []
            for arg, val in frame.f_locals.items():
                if arg == 'self':
                    continue
                val = arg_to_str(val)
                item = f'{arg}={val}'
                items.append(item)
            argstr = ', '.join(items)
            print(f'{obj.__module__}.{obj.__name__}({argstr})')
            print(exctype, value)
            break
        tb = tb.tb_next

OLD_HOOK = None

def set_hook(hook):
    print(f'setting hook to {hook.__name__}')
    OLD_HOOK = sys.excepthook
    sys.excepthook = hook

def unset_hook():
    sys.excepthook = OLD_HOOK

def main():
    set_hook(print_tensors)
    e()
    unset_hook()

if __name__ == '__main__':
    main()



