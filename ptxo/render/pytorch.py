import torch

def tensor_rfunc(ten): 
    shape_str = '[' + ','.join(str(d) for d in ten.shape) + ']'
    dtype_str = str(ten.dtype).split('.')[1]
    dev_str = ten.device.type
    val = f'{shape_str}:{dtype_str}:{dev_str}'
    return val

MAP = { 
        torch.Tensor: tensor_rfunc,
        torch.nn.parameter.Parameter: tensor_rfunc
        }


