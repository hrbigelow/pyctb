import sys
import inspect
import pyctb

if __name__ == '__main__':
    group = sys.argv[1]
    if group == 'torch':
        import torch_test as t
    elif group == 'tf':
         import tf_test as t
    else:
        raise RuntimeError('Only groups `torch` and `tf` are available')
     
    pyctb.add_group(group)
    pyctb.on()
    for name, obj in inspect.getmembers(t, inspect.isfunction):
        print(f'Test: {name}')
        try:
            obj()
        except:
            sys.excepthook(*sys.exc_info())
        print('\n')



        

