import sys
import traceback
from collections import namedtuple
import stack_data 
import inspect
from . import register

RENDERS = { object: repr } # type => render_func

class Config(object):
    def __init__(self):
        self.before = 0
        self.after = 0

CONFIG = Config() 

def inventory():
    """
    List all available registration groups.  Each group defines rendering 
    functions for the listed types.  A group may be added using `add_group`
    """
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

def add(cls, render_func):
    """
    Add `render_func` to be used to render instances of `cls`.  `render_func`
    must have signature:  obj -> str, where isinstance(obj, cls) is true.  You
    may call `add` repeatedly to register handlers for different classes.
    """
    RENDERS[cls] = render_func

def add_group(group):
    """
    Register `group`, a named group of rendering functions associated
    with types.  Use `inventory()` to see available groups.
    """
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

def _convert(val):
    """
    Recursively convert nested values using functions registered in RENDERS.
    """
    vtype = type(val)

    # recursively convert composite types
    if isinstance(val, (tuple, list, set)):
        val = vtype(_convert(v) for v in val)
    elif isinstance(val, dict):
        val = vtype({_convert(k): _convert(v) for k, v in val.items()})
    else:
        rfunc = next(RENDERS[cls] for cls in vtype.__mro__ if cls in RENDERS)
        val = rfunc(val)
    return val

def _argvars(frame_info, exec_node):
    # find all variables which have exec_node as a parent
    vars = []
    for var in frame_info.variables:
        for node in var.nodes:
            if node.parent == exec_node:
                vars.append(var)
    return vars

def _hook(exc_type, exc_value, tb):
    print('Custom Traceback (most recent call last):')
    options = stack_data.Options(before=CONFIG.before, after=CONFIG.after)
    for fi in stack_data.FrameInfo.stack_data(tb, options):
        qname = fi.executing.code_qualname() 
        
        print(f"  File \"{fi.filename}\", line {fi.lineno}, in {qname}")
        # print("-----------")
        for line in fi.lines:
            if line is stack_data.LINE_GAP:
                print("       (...)")
            else:
                # markers = stack_data.markers_from_ranges(
                        # line.executing_node_ranges, convert_ex)
                pfx = '-->' if line.is_current else '   '
                print(f'{pfx} {line.render()}')

        exec_node = fi.executing.node
        if exec_node is not None:
            exec_vars = _argvars(fi, exec_node)
            for var in exec_vars:
                val = _convert(var.value)
                print(f'         {var.name} = {val}')
        tb = tb.tb_next
    traceback.print_exception(exc_type, exc_value, tb)

def config(before_ctx, after_ctx):
    """
    Configure the traceback to display, for each frame, `before_ctx` and
    `after_ctx` pieces of context before (and after) the currently executing
    piece.  A "piece" is defined as in Alex Hall's
    https://github.com/alexmojaki/stack_data repo, it corresponds to one
    logical piece of source code that could be executed.
    """
    CONFIG.before = before_ctx
    CONFIG.after = after_ctx

def on(): 
    """
    Activate pyctb to display the custom traceback during an unhandled
    exception.
    """
    sys.excepthook = _hook

def off():
    """
    Deactivate pyctb.  The default traceback will be displayed upon an
    unhandled exception.
    """
    sys.excepthook = sys.__excepthook__

