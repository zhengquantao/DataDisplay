from functools import reduce
import datetime
print(datetime.date.today())

a = {'a': 1, 'b': 2, 'n': 0, 'c': 3, 'f': 5}


def mul(x):
    return a[x] < 3

m = filter(mul, a)
print(list(m))