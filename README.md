# Python Customized Tracebacks

## Installation

```
pip install pyctb 
```

## Synopsis

```python
import pyctb
# add custom rendering functions
pyctb.add_group('torch')
# activate the custom tracebacks
pyctb.on()

# call your program code, get customized tracebacks if exceptions happen
...
```

## Introduction

pyctb is tool for customizing Python traceback information.  For each traceback
frame, pyctb adds extra lines of the form `var = render(value)` for each
variable in the currently executing function of that frame.  By default,
`render` simply calls `str(value)`.  However, the user may register
sub-functions for rendering specific types of their choice.

You may render a new function to render instances of a class with:

`pyctb.add(cls, func)`

Objects are rendered using the most specific (in method-resolution order)
rendering function registered.  For example:

```python
pyctb.add(Tabby, render_tabby)
pyctb.add(Cat, render_cat)
pyctb.add(Animal, render_animal)
```

Then, a `Tabby` will be rendered with `render_tabby`.  A `Persian` will use
`render_cat`, and `Dog` will use `render_animal`, and so forth.  By default,
`object` is registered with `str`.

## Example

Here you can see an example 

```python

import torch
import pyctb

# show custom render functions for types
pyctb.inventory()
# Returns
# tf:   Render a tf.Tensor, tf.Variable, or EagerTensor
# torch:   Render a torch.Tensor or torch.nn.parameter.Parameter

# generate an exception with default traceback
conv(inp)

# add the torch render group
pyctb.add_group('torch')

# Turn on the custom traceback
pyctb.on()

# generate except with custom traceback showing argument values
conv(inp)

pyctb.off()
```

The tracebacks are as follows:

```python
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/home/henry/miniconda3/envs/pytorch181/lib/python3.9/site-packages/torch/nn/modules/module.py", line 889, in _call_impl
    result = self.forward(*input, **kwargs)
  File "/home/henry/miniconda3/envs/pytorch181/lib/python3.9/site-packages/torch/nn/modules/conv.py", line 263, in forward
    return self._conv_forward(input, self.weight, self.bias)
  File "/home/henry/miniconda3/envs/pytorch181/lib/python3.9/site-packages/torch/nn/modules/conv.py", line 259, in _conv_forward
    return F.conv1d(input, weight, bias, self.stride,
RuntimeError: Expected 3-dimensional input for 3-dimensional weight [5, 5, 10], but got 2-dimensional input of size [5, 100] instead
```

and the customized traceback, using the registered `torch` group:

```python
Custom Traceback (most recent call last):
File "<stdin>", line 1, in <module>
File "/home/henry/miniconda3/envs/pytorch181/lib/python3.9/site-packages/torch/nn/modules/module.py", line 889, in Module._call_impl
     888 else:
-->  889     result = self.forward(*input, **kwargs)
     890 for hook in itertools.chain(
     891         _global_forward_hooks.values(),
     892         self._forward_hooks.values()):
File "/home/henry/miniconda3/envs/pytorch181/lib/python3.9/site-packages/torch/nn/modules/conv.py", line 263, in Conv1d.forward
     262 def forward(self, input: Tensor) -> Tensor:
-->  263     return self._conv_forward(input, self.weight, self.bias)
-->      input = [5,100]:float32:cpu
File "/home/henry/miniconda3/envs/pytorch181/lib/python3.9/site-packages/torch/nn/modules/conv.py", line 259, in Conv1d._conv_forward
     256     return F.conv1d(F.pad(input, self._reversed_padding_repeated_twice, mode=self.padding_mode),
     257                     weight, bias, self.stride,
     258                     _single(0), self.dilation, self.groups)
-->  259 return F.conv1d(input, weight, bias, self.stride,
     260                 self.padding, self.dilation, self.groups)
-->      input = [5,100]:float32:cpu
-->      weight = [5,5,10]:float32:cpu
-->      bias = [5]:float32:cpu
-->      self.stride = ('1',)
-->      self.padding = ('0',)
-->      self.dilation = ('1',)
-->      self.groups = 1
RuntimeError: Expected 3-dimensional input for 3-dimensional weight [5, 5, 10], but got 2-dimensional input of size [5, 100] instead
```

