import traceback
import sys
import torch

OPS = []

for mod in torch.nn.modules.__dict__.values():
    if hasattr(mod, 'forward'):
        OPS.append(mod)

def get_forward_obj(frame):
    """
    Finds an object with a forward method in the current frame's globals
    and whose class is in a registry of classes
    """
    for obj in frame.f_globals.values():
        if obj in OPS and obj.forward.__code__ is frame.f_code:
            return obj
    return None

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

def _print_tensors(exc_type, exc_value, tb):
    print('Traceback (most recent call last):', file=sys.stderr)
    while tb:
        frame = tb.tb_frame
        obj = get_forward_obj(frame)
        if obj is not None:
            items = []
            for arg, val in frame.f_locals.items():
                if arg == 'self':
                    continue
                val = _arg_to_str(val)
                item = f'{arg}={val}'
                items.append(item)
            argstr = ', '.join(items)
            msg = f'    [ptxo]: {obj.__module__}.{obj.__name__}({argstr})'
            print(msg, file=sys.stderr)
        traceback.print_tb(tb, limit=1)
        tb = tb.tb_next
    traceback.print_exception(exc_type, exc_value, tb)

def on(): 
    sys.excepthook = _print_tensors

def off():
    sys.excepthook = sys.__excepthook__

