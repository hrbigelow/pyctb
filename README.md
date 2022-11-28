# Python Customized Tracebacks

## Installation

pip install pyctb 

## Synopsis

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

```python

import torch
import pyctb

# show custom render functions for types
pyctb.inventory()
tf:   Render a tf.Tensor, tf.Variable, or EagerTensor
torch:   Render a torch.Tensor or torch.nn.parameter.Parameter

# add the torch render group
pyctb.add_group('torch')

conv = torch.nn.Conv1d(5, 5, 10)
inp = torch.zeros([5, 100])

# This will produce an exception and the default traceback (see below)
conv(inp)

# Turn on the custom traceback
pyctb.on()

# This will produce the same exception but display a custom traceback
# showing argument values
conv(inp)

pyctb.off()
```

The tracebacks are as follows:

```python
# The default traceback:
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/home/henry/miniconda3/envs/pytorch181/lib/python3.9/site-packages/torch/nn/modules/module.py", line 889, in _call_impl
    result = self.forward(*input, **kwargs)
  File "/home/henry/miniconda3/envs/pytorch181/lib/python3.9/site-packages/torch/nn/modules/conv.py", line 263, in forward
    return self._conv_forward(input, self.weight, self.bias)
  File "/home/henry/miniconda3/envs/pytorch181/lib/python3.9/site-packages/torch/nn/modules/conv.py", line 259, in _conv_forward
    return F.conv1d(input, weight, bias, self.stride,
RuntimeError: Expected 3-dimensional input for 3-dimensional weight [5, 5, 10], but got 2-dimensional input of size [5, 100] instead

# The custom traceback:
Custom Traceback (most recent call last):
  <module>()
  File "<stdin>", line 1, in <module>
  torch.nn.modules.module._call_impl(self=Conv1d(5, 5, kernel_size=(10,), stride=(1,)), input[0]=[5,100]:float32:cpu)
  File "/home/henry/miniconda3/envs/pytorch181/lib/python3.9/site-packages/torch/nn/modules/module.py", line 889, in _call_impl
    result = self.forward(*input, **kwargs)
  torch.nn.modules.conv.forward(self=Conv1d(5, 5, kernel_size=(10,), stride=(1,)), input=[5,100]:float32:cpu)
  File "/home/henry/miniconda3/envs/pytorch181/lib/python3.9/site-packages/torch/nn/modules/conv.py", line 263, in forward
    return self._conv_forward(input, self.weight, self.bias)
  torch.nn.modules.conv._conv_forward(self=Conv1d(5, 5, kernel_size=(10,), stride=(1,)), input=[5,100]:float32:cpu, weight=[5,5,10]:float32:cpu, bias=[5]:float32:cpu)
  File "/home/henry/miniconda3/envs/pytorch181/lib/python3.9/site-packages/torch/nn/modules/conv.py", line 259, in _conv_forward
    return F.conv1d(input, weight, bias, self.stride,
RuntimeError: Expected 3-dimensional input for 3-dimensional weight [5, 5, 10], but got 2-dimensional input of size [5, 100] instead

```




