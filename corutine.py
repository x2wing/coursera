# def chain(*args):
#     for i in args:
#         yield from i


chain  = lambda *args: [(yield from i) for i in args]

def the_same_chain(x_iterable, y_iterable):
    for x in x_iterable:
        yield x
    for y in y_iterable:
        yield y


if __name__ == '__main__':

    a = [1, 2, 3]
    b = (4, 5)
    c = [6, 7, 8, 9, 0]
    for x in chain(a, b, c):
        print(x)
    # for i in yield from [1,2,3]:
