"""
Experiment to see what information is present in the stack trace
How do I get the whole traceback (all frames?)

The frames seem to be only recorded from the first point when an exception is
caught

Difficulty is finding the identity of the caller:

https://stackoverflow.com/questions/2203424/python-how-to-retrieve-class-information-from-a-frame-object

def get_name(frame):
    code = frame.f_code
    name = code.co_name
    for objname, obj in frame.f_globals.items():
        try:
            assert obj.__dict__[name].__code__ is code
        except Exception:
            pass
        else: # obj is the class that defines our method
            name = '%s.%s' % ( objname, name )
            break
    return name
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

