import traceback
import inspect
import sys
import torch
from pprint import pprint

def _arg_to_str(val):
    """
    Recursively convert nested values containing torch.Tensors to a string
    representation of shape:dtype:device.  Use a default string conversion for
    other arguments.
    """
    vtype = type(val)
    if isinstance(val, torch.Tensor):
        ten = val
        shape_str = '[' + ','.join(str(d) for d in ten.shape) + ']'
        dtype_str = str(ten.dtype).split('.')[1]
        dev_str = ten.device.type
        val = f'{shape_str}:{dtype_str}:{dev_str}'
    elif isinstance(val, (tuple, list, set)):
        val = vtype(_arg_to_str(v) for v in val)
    elif isinstance(val, dict):
        val = vtype({_arg_to_str(k): _arg_to_str(v) for k, v in val.items()})
    else:
        val = str(val)
    return val

def _frame_argvals(frame):
    """
    Get formatted argument values as strings.  Preserve the order
    """
    av = inspect.getargvalues(frame)
    items = []
    for arg in av.args:
        val = _arg_to_str(av.locals[arg])
        items.append((arg, val))
    if av.varargs is not None:
        vals = av.locals[av.varargs]
        for pos, val in enumerate(vals):
            arg = f'{av.varargs}[{pos}]'
            val = _arg_to_str(val)
            items.append((arg, val))
    if av.keywords is not None:
        valmap = av.locals[av.keywords]
        for arg, val in valmap.items():
            val = _arg_to_str(val)
            items.append((arg, val))
    return items

def _argvals_hook(exc_type, exc_value, tb):
    print('PTXO Traceback (most recent call last):', file=sys.stderr)
    while tb:
        frame = tb.tb_frame
        args = _frame_argvals(frame)
        mod = inspect.getmodule(frame.f_code)
        name = frame.f_code.co_name
        binds = []

        for arg, val in args:
            bind = f'{arg}={val}'
            binds.append(bind)
        arglist = ', '.join(b for b in binds)
        if mod is None:
            func = name
        else:
            func = f'{mod.__name__}.{name}'
        call = f'  {func}({arglist})'
        print(call, file=sys.stderr)
        traceback.print_tb(tb, limit=1)
        tb = tb.tb_next
    traceback.print_exception(exc_type, exc_value, tb)

def on(): 
    sys.excepthook = _argvals_hook

def off():
    sys.excepthook = sys.__excepthook__

