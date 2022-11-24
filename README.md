# PTXO - PyTorch Op Enhanced Exceptions

## Installation

pip install ptxo

## Synopsis

```python

>>> import torch
>>> import ptxo
>>>
>>> conv = torch.nn.Conv1d(5, 5, 10)
>>> inp = torch.zeros([5, 100])
>>>
>>> conv(inp)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/home/henry/miniconda3/envs/pytorch181/lib/python3.9/site-packages/torch/nn/modules/module.py", line 889, in _call_impl
    result = self.forward(*input, **kwargs)
  File "/home/henry/miniconda3/envs/pytorch181/lib/python3.9/site-packages/torch/nn/modules/conv.py", line 263, in forward
    return self._conv_forward(input, self.weight, self.bias)
  File "/home/henry/miniconda3/envs/pytorch181/lib/python3.9/site-packages/torch/nn/modules/conv.py", line 259, in _conv_forward
    return F.conv1d(input, weight, bias, self.stride,
RuntimeError: Expected 3-dimensional input for 3-dimensional weight [5, 5, 10], but got 2-dimensional input of size [5, 100] instead
>>> ptxo.on()
>>>
>>>
>>>
>>> conv(inp)
PTXO Traceback (most recent call last):
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
>>>

ptxo.off()
```

For each frame in the traceback, pxto adds a line showing the actual values of
arguments in the call as a string representation.  The string representation
may be customized based on type.  Currently the only customization is
displaying all `torch.Tensor` arguments in a format of `shape:dtype:device`.




