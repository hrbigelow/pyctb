from . import rfuncs

def torch():
    """
    Render a Torch tensor and Parameter
    Second line
    """
    import torch
    fmap = {
            torch.Tensor: rfuncs.torch_tensor,
            torch.nn.parameter.Parameter: rfuncs.torch_tensor 
    }
    return fmap 

def tf():
    """
    Render a tf.Tensor or tf.Variable
    """
    import tensorflow as tf
    fmap = {
            tf.Tensor: rfuncs.tf_tensor,
            tf.Variable: rfuncs.tf_tensor 
            }
    return fmap

