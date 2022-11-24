"""
https://stackoverflow.com/questions/2203424/python-how-to-retrieve-class-information-from-a-frame-object

"""
import torch
import ptxo
import sys

conv = torch.nn.Conv1d(5, 5, 10)

def run():
    inp = torch.zeros([5, 100])
    return conv(inp)

def main():
    use_hook = (sys.argv[1] == 'y')
    if use_hook:
        ptxo.on()
    run()

    if use_hook:
        ptxo.off()

if __name__ == '__main__':
    main()

