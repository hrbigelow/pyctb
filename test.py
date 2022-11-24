"""
https://stackoverflow.com/questions/2203424/python-how-to-retrieve-class-information-from-a-frame-object

"""
import pyctb 
import sys

def torch_test():
    import torch
    conv = torch.nn.Conv1d(5, 5, 10)
    inp = torch.zeros([5, 100])
    conv(inp)

def tf_test():
    import tensorflow as tf
    a = tf.random.uniform([3,5,7], 0, 100, dtype=tf.float32)
    b = tf.random.uniform([3,5,7], 0, 100, dtype=tf.float32)
    return tf.matmul(a, b)

def run(mode, func):
    """
    Runs the func under normal and pyctb exception hooks
    """
    pyctb.add(mode)
    print(f'Testing {mode}')
    print('Normal traceback:')
    try:
        func()
    except:
        sys.excepthook(*sys.exc_info())
        pass

    pyctb.on()
    print('\n\nCustom traceback:')
    try:
        func()
    except:
        sys.excepthook(*sys.exc_info())
        pass

def main():
    mode = sys.argv[1]
    if mode == 'torch':
        run(mode, torch_test)
    elif mode == 'tf':
        run(mode, tf_test)
    else:
        print(f'unknown mode {mode}')

if __name__ == '__main__':
    main()

