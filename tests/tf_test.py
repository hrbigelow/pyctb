import sys
import tensorflow as tf
import pyctb

def matmul_test():
    a = tf.random.uniform([3,5,7], 0, 100, dtype=tf.float32)
    b = tf.random.uniform([3,5,7], 0, 100, dtype=tf.float32)
    return tf.matmul(a, 
            b)

def binop_test():
    a = tf.random.uniform([3,5,7], 0, 100, dtype=tf.float32)
    b = tf.random.uniform([3,6,7], 0, 100, dtype=tf.float32)
    c = a / b
    return c

def add(a, b):
    return a + b

def fadd(a, b):
    return 'fake'

def test3():
    return add(add(2, 4), fadd(3, 5))

def main(before_context, after_context):
    pyctb.add_group('tf')
    pyctb.config(before_context, after_context)
    for test in (matmul_test, binop_test, test3):
        pyctb.off()
        print(f'============== {test.__name__} ==============')
        try:
            test()
        except:
            sys.excepthook(*sys.exc_info())
        print('\n')
        pyctb.on()
        try:
            test()
        except:
            sys.excepthook(*sys.exc_info())
        print('\n\n')

if __name__ == '__main__':
    before = int(sys.argv[1])
    after = int(sys.argv[2])
    main(before, after)

