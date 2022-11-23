"""
Experiment to see what information is present in the stack trace
How do I get the whole traceback (all frames?)

The frames seem to be only recorded from the first point when an exception is
caught

"""
import sys
import torch

def a(man, chi):
    raise BaseException('a')

conv = torch.nn.Conv1d(5, 5, 10)

def b(ace, jar):
    inp = torch.zeros([5, 100])
    return conv(inp)
    # return a(6, {'a', 'b'})

def c(foo, bar):
    return b('abce', [5,3,1])

def d(yab, tab):
    try:
        return c('a', 'baz')
    except BaseException as ex:
        raise ex

def d(yab, tab):
    return c(5, 'a')

def e(*args):
    return d('c', [1,2,3])

def f(*args):
    return e({}, 'abc')


def thr(arg):
    raise BaseException(arg)

def trycatchraise():
    try:
        thr()
    except BaseException as ex:
        raise BaseException(f'trycatchraise: {ex}')

def trycatch():
    try:
        thr()
    except BaseException as ex:
        return 10

OPS = { torch.nn.modules.conv.Conv1d }

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
        code = frame.f_code
        locs = frame.f_locals
        caller = locs.get('self', None)
        if type(caller) in OPS:
            items = []
            for arg, val in locs.items():
                if arg == 'self':
                    continue
                val = arg_to_str(val)
                item = f'{arg}={val}'
                items.append(item)
            argstr = ', '.join(items)
            print(f'{type(caller).__name__}({argstr})')
        tb = tb.tb_next

OLD_HOOK = None

def set_hook(hook):
    OLD_HOOK = sys.excepthook
    sys.excepthook = hook

def unset_hook():
    sys.excepthook = OLD_HOOK

def main():
    set_hook(print_tensors)
    f()
    unset_hook()

if __name__ == '__main__':
    main()



