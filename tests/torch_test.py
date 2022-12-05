import torch

def matmul_test():
    a = torch.randn(3,5,7)
    b = torch.randn(3,5,7)
    return torch.matmul(a, b)

def binop_test():
    a = torch.randn(3,5,7)
    b = torch.randn(3,6,7)
    return a / b

