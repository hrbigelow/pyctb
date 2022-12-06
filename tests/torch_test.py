import sys
import torch
import pyctb

def matmul_test():
    a = torch.randn(3,5,7)
    b = torch.randn(3,5,7)
    c = b * 5 
    d = torch.matmul(a, b)
    e = d - 5
    return e

def binop_test():
    a = torch.randn(3,5,7)
    b = torch.randn(3,6,7)
    return a / b

def main(before_context, after_context):
    pyctb.add_group('torch')
    pyctb.config(before_context, after_context)
    for test in (binop_test, matmul_test):
        pyctb.off()
        print(f'========= Default traceback for {test.__name__} =========')
        try:
            test()
        except:
            sys.excepthook(*sys.exc_info())
        print('\n')
        print(f'========= Custom traceback for {test.__name__} =========')
        print(f'{pyctb.CONFIG.before} pieces of leading context')
        print(f'{pyctb.CONFIG.after} pieces of trailing context')
        pyctb.on()
        try:
            test()
        except:
            sys.excepthook(*sys.exc_info())
        print('\n')

if __name__ == '__main__':
    before = int(sys.argv[1])
    after = int(sys.argv[2])
    main(before, after)


