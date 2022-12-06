# Python Customized Tracebacks

## Installation

```
pip install pyctb 
```

## Synopsis

```python
import pyctb

# add a pre-existing group of custom rendering functions
pyctb.add_group('torch')

# or add your own:
# pyctb.add(your_cls, your_render_func)
# pyctb.add(your_cls2, your_render_func2)
# ...

# for each frame in the traceback:
# display 1 piece of code context before the current executing piece
# display 0 pieces of code context after the current executing piece
pyctb.config(before_ctx=1, after_ctx=0)

# activate the custom tracebacks
pyctb.on()

# your program code below.  any exception will generate a customized traceback
...

# exceptions will now generate the default traceback as before
pyctb.off()
```

## Introduction

pyctb is tool for customizing the information displayed in a Python traceback.
It is useful to quickly see the values of arguments or operands used at the
point where your program throws an exception, without the need for a debugger.
For each traceback frame, pyctb adds extra lines of the form `var =
render_func(value)` for each variable in the currently executing function of
that frame, using a `render_func` registered with that class.  By default,
`object` is registered to use `repr`.  The user may register custom functions for
rendering specific types of their choice.  Such specific rendering functions
are needed for types that have too large of an output with just `repr`.

pyctb relies on the excellent
[stack_data](https://github.com/alexmojaki/stack_data) repo from Alex Hall for
inspecting the frame information variable names and values.

You may register a new rendering function using:

`pyctb.add(cls, func)`

Objects are rendered using the most specific (in method-resolution order)
rendering function registered.  For example:

```python
pyctb.add(Animal, render_animal)
pyctb.add(Cat, render_cat)
pyctb.add(Tabby, render_tabby)
```

Then, a `Tabby` will be rendered with `render_tabby`.  A `Persian` will use
`render_cat`, and `Dog` will use `render_animal`, and so forth.  By default,
`object` is registered with `repr`.

## Tests

```bash
# compare default and customized tracebacks using the `torch` group of
# renderers.  In each frame of the traceback, <before_ctx> and <after_ctx>
# specify the number of pieces of code context to be displayed before and after
# each currently executing piece.  Using 0 for both <before_ctx> and
# <after_ctx> is equivalent to the default behavior.
python -m tests.torch_test <before_ctx> <after_ctx>

# same but with tensorflow tests.
python -m tests.tf_test <before_ctx> <after_ctx>
```

The `tests.torch_test` runs two functions called `binop_test` and
`matmul_test`.  Each function raises an exception, and it is run twice.  First
with `pyctb` turned off, and then with it turned on.  The default and custom
tracebacks are shown as output.

Notice that the custom traceback provides additional `name = value` lines for
all arguments to the function or operand that raised the exception.  In this
case, using the `torch` group, the operands were `torch.Tensor`, and the custom
rendering function displays them in a format `shape:dtype:device`.

Additionally, you can see that there is one piece of leading code context (if
it exists in that frame) shown before the currently executing piece.

```
# Run the torch_tests using 1 piece of leading context and non trailing context
(pytorch181) henry@henry-gs65:pyctb$ python -m tests.torch_test 1 0
========= Default traceback for binop_test =========
Traceback (most recent call last):
  File "/home/henry/ai/projects/pyctb/tests/torch_test.py", line 25, in main
    test()
  File "/home/henry/ai/projects/pyctb/tests/torch_test.py", line 16, in binop_test
    return a / b
RuntimeError: The size of tensor a (5) must match the size of tensor b (6) at non-singleton dimension 1


========= Custom traceback for binop_test =========
1 pieces of leading context
0 pieces of trailing context
Custom Traceback (most recent call last):
  File "/home/henry/ai/projects/pyctb/tests/torch_test.py", line 34, in main
    try:
-->     test()
         test = <function binop_test at 0x7f86bbfeda60>
  File "/home/henry/ai/projects/pyctb/tests/torch_test.py", line 16, in binop_test
    b = torch.randn(3,6,7)
--> return a / b
         a = [3,5,7]:float32:cpu
         b = [3,6,7]:float32:cpu
RuntimeError: The size of tensor a (5) must match the size of tensor b (6) at non-singleton dimension 1


========= Default traceback for matmul_test =========
Traceback (most recent call last):
  File "/home/henry/ai/projects/pyctb/tests/torch_test.py", line 25, in main
    test()
  File "/home/henry/ai/projects/pyctb/tests/torch_test.py", line 9, in matmul_test
    d = torch.matmul(a, b)
RuntimeError: Expected batch2_sizes[0] == bs && batch2_sizes[1] == contraction_size to be true, but got false.  (Could this error message be improved?  If so, please report an enhancement request to PyTorch.)


========= Custom traceback for matmul_test =========
1 pieces of leading context
0 pieces of trailing context
Custom Traceback (most recent call last):
  File "/home/henry/ai/projects/pyctb/tests/torch_test.py", line 34, in main
    try:
-->     test()
         test = <function matmul_test at 0x7f87e7ce8c10>
  File "/home/henry/ai/projects/pyctb/tests/torch_test.py", line 9, in matmul_test
    c = b * 5
--> d = torch.matmul(a, b)
         a = [3,5,7]:float32:cpu
         b = [3,5,7]:float32:cpu
RuntimeError: Expected batch2_sizes[0] == bs && batch2_sizes[1] == contraction_size to be true, but got false.  (Could this error message be improved?  If so, please report an enhancement request to PyTorch.)
```


