from function import get_function
from rational import Rational


def test_divide_and_conquer():
    func1 = 'T(n) = 2T(n/2) + Theta(n)'
    func2 = 'T(n) = 7T(n/2) + Theta(n^2)'
    func3 = 'T(n) = 3T(n/4) + cn^2'

    func1_obj = get_function(func1)
    assert func1_obj.a == 2
    assert func1_obj.b == Rational('2')
    assert func1_obj.c == 'c'
    assert func1_obj.d == Rational('1')

    func2_obj = get_function(func2)
    assert func2_obj.a == 7
    assert func2_obj.b == Rational('2')
    assert func2_obj.c == 'c'
    assert func2_obj.d == Rational('2')

    func3_obj = get_function(func3)
    assert func3_obj.a == 3
    assert func3_obj.b == Rational('4')
    assert func3_obj.c == 'c'
    assert func3_obj.d == Rational('2')


def test_chip_and_be_conquered():
    func1 = 'T(n) = T(n-1) + n'
    func2 = 'T(n) = 2T(n-1) + 1'
    func3 = 'T(n) = T(n-2) + n^2'

    func1_obj = get_function(func1)
    assert func1_obj.a == 1
    assert func1_obj.b == Rational('1')
    assert func1_obj.c == Rational('1')
    assert func1_obj.d == Rational('1')

    func2_obj = get_function(func2)
    assert func2_obj.a == 2
    assert func2_obj.b == Rational('1')
    assert func2_obj.c == Rational('1')
    assert func2_obj.d == Rational('1')

    func3_obj = get_function(func3)
    assert func3_obj.a == 1
    assert func3_obj.b == Rational('2')
    assert func3_obj.c == Rational('1')
    assert func3_obj.d == Rational('2')
