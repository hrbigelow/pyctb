import importlib
import traceback
import inspect
import sys
from . import register

RENDERS = {} # type => render_func

def inventory():
    funcs = {}
    for name, obj in inspect.getmembers(register, inspect.isfunction):
        doc = inspect.getdoc(obj)
        funcs[name] = doc.split('\n')
    # Print out in tabular format
    rows = []
    for name, doclines in funcs.items():
        gap = ' ' * (len(name) + 1)
        hdr = f'{name}:'
        for line in doclines:
            row = f'{hdr}   {line}'
            rows.append(row)
            hdr = gap
        rows.append('')
    final = '\n'.join(rows)
    print(final)

def add(group):
    regfunc = inspect.getattr_static(register, group, None)
    if regfunc is None:
        raise ValueError(
                f'Requested \'{group}\' which does not exist in the inventory. '
                f'Use inventory() function to see all options.')
    try:
        fmap = regfunc()
    except BaseException as ex:
        raise ValueError(
            f'Error when attempting to register render group \'{group}\': {ex}')
    RENDERS.update(fmap)

def _arg_to_str(val):
    """
    Recursively convert nested values using functions registered in RENDERS.
    """
    vtype = type(val)
    rfunc = RENDERS.get(vtype, None)
    if rfunc is not None:
        val = rfunc(val)
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

