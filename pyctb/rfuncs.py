def tf_tensor(ten):
    # Render a tensorflow tensor
    shape_str = '[' + ','.join(map(str, ten.shape)) + ']'
    dtype_str = ten.dtype.name
    dev_str = ten.device
    val = f'{shape_str}:{dtype_str}:{dev_str}'
    return val


def torch_tensor(ten): 
    # Render a pytorch tensor
    shape_str = '[' + ','.join(map(str, ten.shape)) + ']'
    dtype_str = str(ten.dtype).split('.')[1]
    dev_str = ten.device.type
    val = f'{shape_str}:{dtype_str}:{dev_str}'
    return val


