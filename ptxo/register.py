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
    from tensorflow.python.framework.ops import EagerTensor
    fmap = {
            EagerTensor: rfuncs.tf_tensor,
            tf.Tensor: rfuncs.tf_tensor,
            tf.Variable: rfuncs.tf_tensor 
            }

    return fmap

