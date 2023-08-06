import math

# primitive types
int_test1 = 69
int_test2 = -12
float_test1 = 1.5
float_test2 = -1.5
bool_test1 = False
bool_test2 = True
none_test = None
str_test1 = 'Hello'
str_test2 = 'Bye'
complex_test = complex(7, 8)

# collection types
list_test1 = [4, 145, 0.01]
list_test2 = [4, "dff", 0.01]
list_test3 = [4, "dff", None, 0.22]

tuple_test1 = (4, 145, 0.01)
tuple_test2 = (4, "dff", 0.01)
tuple_test3 = (4, "dff", None, 0.22)

set_test1 = {4, 145, 0.01}
set_test2 = {4, "dff", 0.01}
set_test3 = {4, "dff", None, 0.22}

dict_test1 = {'Club': 'Chelsea', 'Titles': 100, 'CL': True}
dict_test2 = {1: ["h", 2], 2: (1, 21), 3: '3', 4: True}
dict_test3 = {5: ["h", 2, (3, 4, {5, 6, '7', True})], 6: (1, (2, (3, (4, (5, (6, (7)))))))}

# functions
def foo1():
    return int_test1


def foo2(param):
    return int_test2 + param


def foo3(*param):
    res = 0
    for el in param:
        res += el
    return res


def foo4(param):
    return math.atan(param) + math.cos(param)


def foo5(list):
    return sorted(list)


def foo6(num):
    if num == 1:
        return 1
    else:
        return num + foo6(num - 1)


lambda_fanc1 = lambda num: num + 2
lambda_fanc2 = lambda num, n: num**n


class A:
    num1 = 12

    def __init__(self):
        pass

    def foo(self, num):
        return num


class B(A):
    num2 = 12

    def __init__(self, num2):
        self.num2 = num2

    def boo(self):
        return 222

class Foo1:
    def __init__(self):
        pass

    def foo(self, n):
        return n


class Foo2:

    def __init__(self):
        pass

    def foo(self, n):
        return 2*n


class Stadium:
    matches_count = 0

    def __init__(self, name, capacity, spectators):
        self.name = name
        self.capacity = capacity
        self.spectators = spectators
        Stadium.matches_count += 1

    def display_count(self):
        print('ALL employees amount: %d' % Stadium.matches_count)

def dec(foo):
    def wr(*args, **kwargs):
        return 10 * foo(*args, **kwargs)
    return wr

def for_dec(a):
    return 2 * a

decorated_func = dec(for_dec)


class Q(type):
    def __new__(cls, name, bases, attrs):
        attrs['my_attrs'] = "TestMessage"

        return super().__new__(cls, name, bases, attrs)


class W(metaclass=Q):
    pass