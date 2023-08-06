from serializers.factory import Factory
from test_value import *

serializer = Factory.create_serializer(".json")


def test_1():
    assert int_test1 == serializer.loads(serializer.dumps(int_test1))


def test_2():
    assert int_test2 == serializer.loads(serializer.dumps(int_test2))


def test_3():
    assert float_test1 == serializer.loads(serializer.dumps(float_test1))


def test_4():
    assert float_test2 == serializer.loads(serializer.dumps(float_test2))


def test_5():
    assert bool_test1 == serializer.loads(serializer.dumps(bool_test1))


def test_6():
    assert bool_test2 == serializer.loads(serializer.dumps(bool_test2))


def test_7():
    assert str_test1 == serializer.loads(serializer.dumps(str_test1))


def test_8():
    assert str_test2 == serializer.loads(serializer.dumps(str_test2))


def test_9():
    assert none_test == serializer.loads(serializer.dumps(none_test))


def test_10():
    assert complex_test == serializer.loads(serializer.dumps(complex_test ))


def test_11():
    assert list_test1 == serializer.loads(serializer.dumps(list_test1))


def test_12():
    assert list_test2 == serializer.loads(serializer.dumps(list_test2))


def test_13():
    assert list_test3 == serializer.loads(serializer.dumps(list_test3))


def test_14():
    assert tuple_test1 == serializer.loads(serializer.dumps(tuple_test1))


def test_15():
    assert tuple_test2 == serializer.loads(serializer.dumps(tuple_test2))


def test_16():
    assert tuple_test3 == serializer.loads(serializer.dumps(tuple_test3))


def test_17():
    assert set_test1 == serializer.loads(serializer.dumps(set_test1))


def test_18():
    assert set_test2 == serializer.loads(serializer.dumps(set_test2))


def test_19():
    assert set_test3 == serializer.loads(serializer.dumps(set_test3))


def test_20():
    assert dict_test1 == serializer.loads(serializer.dumps(dict_test1))


def test_21():
    assert dict_test2 == serializer.loads(serializer.dumps(dict_test2))


def test_22():
    assert dict_test3 == serializer.loads(serializer.dumps(dict_test3))


def test_23():
    assert foo1() == serializer.loads(serializer.dumps(foo1))()


def test_24():
    assert foo2(12) == serializer.loads(serializer.dumps(foo2))(12)


def test_25():
    assert foo3(12) == serializer.loads(serializer.dumps(foo3))(12)


def test_26():
    assert foo3(1, 1, 1, 1, 1) == serializer.loads(serializer.dumps(foo3))(1, 1, 1, 1, 1)


def test_27():
    assert foo4(12) == serializer.loads(serializer.dumps(foo4))(12)


def test_28():
    assert foo5([41, 16, 5, 18]) == serializer.loads(serializer.dumps(foo5))([41, 16, 5, 18])


def test_29():
    assert foo6(5) == serializer.loads(serializer.dumps(foo6))(5)


def test_30():
    tmp = serializer.loads(serializer.dumps(lambda_fanc1))
    assert tmp(18) == lambda_fanc1(18)


def test_31():
    tmp = serializer.loads(serializer.dumps(lambda_fanc2))
    assert tmp(12, 2) == lambda_fanc2(12, 2)


def test_32():
    tmp = serializer.loads(serializer.dumps(A))
    tmp = tmp()
    a = A()

    assert a.num1 == tmp.num1
    assert a.foo(4) == tmp.foo(4)


def test_33():
    tmp = serializer.loads(serializer.dumps(B))
    tmp = tmp(2)
    b = B(2)

    assert tmp.num1 == b.num1
    assert tmp.boo() == b.boo()
    assert tmp.foo(4) == b.foo(4)


def test_34():
    tmp = serializer.loads(serializer.dumps(Foo1))
    f1 = tmp()
    foo1 = Foo1()

    tmp = serializer.loads(serializer.dumps(Foo2))
    f2 = tmp()
    foo2 = Foo2()

    assert f2.foo(4) == foo2.foo(4)
    assert f1.foo(4) * 2 == f2.foo(4)


def test_35():
    a = A()
    tmp = serializer.loads(serializer.dumps(a))

    assert tmp.num1 == a.num1
    assert tmp.foo(4) == a.foo(4)


def test_36():
    df = serializer.dumps(decorated_func)
    df = serializer.loads(df)
    before = [decorated_func(i) for i in range(100)]
    after = [df(i) for i in range(100)]
    assert before == after

def test_37():
    assert serializer.loads(serializer.dumps(W().my_attrs)) == W().my_attrs