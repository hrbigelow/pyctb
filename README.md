# PTXO - PyTorch Op Enhanced Exceptions

## Synopsis

```python

import torch
import ptxo

conv = torch.nn.Conv1d(5, 5, 10)
inp = torch.zeros([5, 100])

conv(inp)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "...site-packages/torch/nn/modules/module.py", line 889, in _call_impl
    result = self.forward(*input, **kwargs)
  File "...site-packages/torch/nn/modules/conv.py", line 263, in forward
    return self._conv_forward(input, self.weight, self.bias)
  File "...site-packages/torch/nn/modules/conv.py", line 259, in _conv_forward
    return F.conv1d(input, weight, bias, self.stride,
RuntimeError: Expected 3-dimensional input for 3-dimensional weight [5, 5, 10],\
        but got 2-dimensional input of size [5, 100] instead

# Turn on the exception interceptor
ptxo.on()

conv(inp)
  File "<stdin>", line 1, in <module>
  File "...site-packages/torch/nn/modules/module.py", line 889, in _call_impl
    result = self.forward(*input, **kwargs)
    [ptxo]: torch.nn.modules.conv.Conv1d(input=[5,100]:float32:cpu)
  File "...site-packages/torch/nn/modules/conv.py", line 263, in forward
    return self._conv_forward(input, self.weight, self.bias)
  File "...site-packages/torch/nn/modules/conv.py", line 259, in _conv_forward
    return F.conv1d(input, weight, bias, self.stride,
RuntimeError: Expected 3-dimensional input for 3-dimensional weight [5, 5, 10],\
        but got 2-dimensional input of size [5, 100] instead

ptxo.off()
```

The backtrace is almost identical, but there is one extra line, which shows
argument names and values of the PyTorch function which caused an exception.
Tensor values are shown as shape:dtype:device strings.

    `[ptxo]: torch.nn.modules.conv.Conv1d(input=[5,100]:float32:cpu)`



