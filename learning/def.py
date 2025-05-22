import os

def main(opt):
    if opt == 1:
        ret = first()
    elif opt == 2:
        ret = second()
    else:
        ret = first()

def first():
    print('First')

def second():
    print('Second')