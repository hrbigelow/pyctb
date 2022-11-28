import tensorflow as tf

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

