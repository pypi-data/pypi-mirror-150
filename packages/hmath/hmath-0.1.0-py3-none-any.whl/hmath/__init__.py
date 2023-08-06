# -*- coding: utf-8 -*-
# hmath
# by caleb7023

import sys
from functools import lru_cache

@lru_cache(maxsize=None)
def inf():
    return float("inf")

@lru_cache(maxsize=None)
def complex_test(_x):
    try:
        a = _x.imag
        if a == 0:
            return False
        else:
            return True
    except:
        return True

@lru_cache(maxsize=None)
def primality_test(_n):
    root_n = _n ** 0.5
    divisible = True
    for test in range(int(root_n) - 1):
        if  int(_n / (test + 2)) == _n / (test + 2):
            divisible = False
            break
    return divisible

@lru_cache(maxsize=None)
def prime_factorization(_n):
    if primality_test(_n):
        return _n
    decomposition_result = []
    prime_factorization2_ans_1 = _n
    prime_factorization2_ans_2 = 1
    while not(prime_factorization2_ans_1 == 1):
        for k in range(2 , int(prime_factorization2_ans_1 ** 0.5) + 1):
            if prime_factorization2_ans_1 / k == prime_factorization2_ans_1 // k / 1:
                if primality_test(k):
                    prime_factorization2_ans_2 = k
                    break
        prime_factorization2_ans_1 = prime_factorization2_ans_1 / prime_factorization2_ans_2
        if not(prime_factorization2_ans_2 == 1):
            decomposition_result += [str(int(prime_factorization2_ans_2))]
    return decomposition_result

@lru_cache(maxsize=None)
def division(_x , _y):
    if _y == 0:
        if   0 < _x:
            return  inf()
        elif _x < 0:
            return -inf()
        else:
            return  0
    elif _y == inf():
        return 0
    else:
        return _x / _y

@lru_cache(maxsize=None)
def imaginary_part(_x):
    try:
        return _x.imag
    except:
        return 0

@lru_cache(maxsize=None)
def real_part(_x):
    try:
        return _x.real
    except:
        return 0

@lru_cache(maxsize=None)
def pi():
    return 3.1415926535897932384626433832795

@lru_cache(maxsize=None)
def e():
    return 2.7182818284590452353602874713527

@lru_cache(maxsize=None)
def phi(): # φ
    return 1.6180339887498948482045868343656

@lru_cache(maxsize=None)
def C(): #Euler's gamma
    return 0.5772156649015328606065120900824

@lru_cache(maxsize=None)
def exp(_x):
    return e() ** _x

@lru_cache(maxsize=None)
def ln(_x):
    value_2 = 0
    for n in range(1 , 2000):
        value_3 = 2 ** (-n)
        value_2 += division(value_3 * (_x ** value_3), 1 + (_x ** value_3))
    return division(1 , division(_x , _x - 1) - value_2)

@lru_cache(maxsize=None)
def log(_x , _y):
    return division(ln(_y) , ln(_x))

@lru_cache(maxsize=None)
def square_root(_x):
    return _x ** 0.5

@lru_cache(maxsize=None)
def cube_root(_x):
    return _x ** 0.3333333333333333333333333333333333333333

@lru_cache(maxsize=None)
def root_of(_x , _y):
    return _y ** (1 / _x)

@lru_cache(maxsize=None)
def gamma(_x):
    value_1 = 1
    for n in range(1 , 100000):
        value_1 *= division(((1 + (1 / n)) ** _x) , (1 + (_x / n)))
    return 1 / _x * value_1

@lru_cache(maxsize=None)
def factorial(_x):
    if not complex_test(_x):
        if _x % 1 == 0 and 0 < _x:
            ans = 1
            for process in range(1 , _x + 1):
                ans = ans * process
            return ans
    return gamma(_x + 1)

@lru_cache(maxsize=None)
def sin(_θ):
    return (exp(1j * _θ) - exp(-(1j * _θ))) / 2j

@lru_cache(maxsize=None)
def cos(_θ):
    return (exp(1j * _θ) + exp(-(1j * _θ))) / 2

@lru_cache(maxsize=None)
def tan(_θ):
    return division(sin(_θ) , cos(_θ))

@lru_cache(maxsize=None)
def csc(_θ):
    return division(1 , sin(_θ))

@lru_cache(maxsize=None)
def sec(_θ):
    return division(1 , cos(_θ))

@lru_cache(maxsize=None)
def cot(_θ):
    return division(1 , tan(_θ))

@lru_cache(maxsize=None)
def asin(_x):
    return -1j * ln(1j * _x + square_root(1 - (_x ** 2)))

@lru_cache(maxsize=None)
def acos(_x):
    return -1j * ln(_x - 1j * square_root(1 - (_x ** 2)))

@lru_cache(maxsize=None)
def atan(_x):
    return 1j * (ln(1 - _x * 1j) - ln(1 + _x * 1j)) / 2

@lru_cache(maxsize=None)
def acsc(_x):
    return asin(division(1 , _x))

@lru_cache(maxsize=None)
def asec(_x):
    return acos(division(1 , _x))

@lru_cache(maxsize=None)
def acot(_x):
    return atan(division(1 , _x))

@lru_cache(maxsize=None)
def sinh(_x):
    return (exp(_x) - exp(-_x)) / 2

@lru_cache(maxsize=None)
def cosh(_x):
    return (exp(_x) + exp(-_x)) / 2

@lru_cache(maxsize=None)
def tanh(_x):
    return sinh(_x) / cosh(_x)

@lru_cache(maxsize=None)
def csch(_x):
    return 1 / sinh(_x)

@lru_cache(maxsize=None)
def sech(_x):
    return 1 / cosh(_x)

@lru_cache(maxsize=None)
def coth(_x):
    return 1 / tanh(_x)

@lru_cache(maxsize=None)
def asinh(_x):
    return ln(_x + square_root((_x ** 2) + 1))

@lru_cache(maxsize=None)
def acosh(_x):
    return ln(_x + square_root((_x + 1) * (_x - 1)))

@lru_cache(maxsize=None)
def atanh(_x):
    return ln((1 + _x) / (1 - _x)) / 2

@lru_cache(maxsize=None)
def acsch(_x):
    return asinh(1 / _x)

@lru_cache(maxsize=None)
def asech(_x):
    return acosh(1 / _x)

@lru_cache(maxsize=None)
def acoth(_x):
    return atanh(1 / _x)

@lru_cache(maxsize=None)
def radian(_θ):
    return _θ * 57.295779513082320876798154814105

@lru_cache(maxsize=None)
def degrees(_θ):
    return _θ / 57.295779513082320876798154814105

@lru_cache(maxsize=None)
def sinT(_n , _θ):
    if type(_n)==str:
        k = 0.01
        ans = _θ
        for h in range(len(_n)):
            if _n[h] == "d":
                ans = (sin(ans + k) - sin(ans)) / k
            else:
                raise Exception('The value of the argument must be a string that contains only "d" or a natural number.')
        return ans
    elif _n <= 0 or not _n % 1 == 0:
        raise Exception('The value of the argument must be a string that contains only "d" or a natural number.')
    else:
        ans = _θ
        for k in range(_n + 1):
            ans = sin(ans)
    return ans

@lru_cache(maxsize=None)
def cosT(_n , _θ):
    if type(_n)==str:
        k = 0.01
        ans = _θ
        for h in range(len(_n)):
            if _n[h] == "d":
                ans = (cos(ans + k) - cos(ans)) / k
            else:
                raise Exception('The value of the argument must be a string that contains only "d" or a natural number.')
        return ans
    elif _n <= 0 or not _n % 1 == 0:
        raise Exception('The value of the argument must be a string that contains only "d" or a natural number.')
    else:
        ans = _θ
        for k in range(_n + 1):
            ans = cos(ans)
    return ans

@lru_cache(maxsize=None)
def tanT(_n , _θ):
    if type(_n)==str:
        k = 0.01
        ans = _θ
        for h in range(len(_n)):
            if _n[h] == "d":
                ans = (tan(ans + k) - tan(ans)) / k
            else:
                raise Exception('The value of the argument must be a string that contains only "d" or a natural number.')
        return ans
    elif _n <= 0 or not _n % 1 == 0:
        raise Exception('The value of the argument must be a string that contains only "d" or a natural number.')
    else:
        ans = _θ
        for k in range(_n + 1):
            ans = tan(ans)
    return ans

@lru_cache(maxsize=None)
def cscT(_n , _θ):
    if type(_n)==str:
        k = 0.01
        ans = _θ
        for h in range(len(_n)):
            if _n[h] == "d":
                ans = (csc(ans + k) - csc(ans)) / k
            else:
                raise Exception('The value of the argument must be a string that contains only "d" or a natural number.')
        return ans
    elif _n <= 0 or not _n % 1 == 0:
        raise Exception('The value of the argument must be a string that contains only "d" or a natural number.')
    else:
        ans = _θ
        for k in range(_n + 1):
            ans = csc(ans)
    return ans

@lru_cache(maxsize=None)
def secT(_n , _θ):
    if type(_n)==str:
        k = 0.01
        ans = _θ
        for h in range(len(_n)):
            if _n[h] == "d":
                ans = (sec(ans + k) - sec(ans)) / k
            else:
                raise Exception('The value of the argument must be a string that contains only "d" or a natural number.')
        return ans
    elif _n <= 0 or not _n % 1 == 0:
        raise Exception('The value of the argument must be a string that contains only "d" or a natural number.')
    else:
        ans = _θ
        for k in range(_n + 1):
            ans = sec(ans)
    return ans

@lru_cache(maxsize=None)
def cotT(_n , _θ):
    if type(_n)==str:
        k = 0.01
        ans = _θ
        for h in range(len(_n)):
            if _n[h] == "d":
                ans = (cot(ans + k) - cot(ans)) / k
            else:
                raise Exception('The value of the argument must be a string that contains only "d" or a natural number.')
        return ans
    elif _n <= 0 or not _n % 1 == 0:
        raise Exception('The value of the argument must be a string that contains only "d" or a natural number.')
    else:
        ans = _θ
        for k in range(_n + 1):
            ans = cot(ans)
    return ans

@lru_cache(maxsize=None)
def asinT(_n , _θ):
    if type(_n)==str:
        k = 0.01
        ans = _θ
        for h in range(len(_n)):
            if _n[h] == "d":
                ans = (asin(ans + k) - asin(ans)) / k
            else:
                raise Exception('The value of the argument must be a string that contains only "d" or a natural number.')
        return ans
    elif _n <= 0 or not _n % 1 == 0:
        raise Exception('The value of the argument must be a string that contains only "d" or a natural number.')
    else:
        ans = _θ
        for k in range(_n + 1):
            ans = asin(ans)
    return ans

@lru_cache(maxsize=None)
def acosT(_n , _θ):
    if type(_n)==str:
        k = 0.01
        ans = _θ
        for h in range(len(_n)):
            if _n[h] == "d":
                ans = (acos(ans + k) - acos(ans)) / k
            else:
                raise Exception('The value of the argument must be a string that contains only "d" or a natural number.')
        return ans
    elif _n <= 0 or not _n % 1 == 0:
        raise Exception('The value of the argument must be a string that contains only "d" or a natural number.')
    else:
        ans = _θ
        for k in range(_n + 1):
            ans = acos(ans)
    return ans

@lru_cache(maxsize=None)
def atanT(_n , _θ):
    if type(_n)==str:
        k = 0.01
        ans = _θ
        for h in range(len(_n)):
            if _n[h] == "d":
                ans = (atan(ans + k) - atan(ans)) / k
            else:
                raise Exception('The value of the argument must be a string that contains only "d" or a natural number.')
        return ans
    elif _n <= 0 or not _n % 1 == 0:
        raise Exception('The value of the argument must be a string that contains only "d" or a natural number.')
    else:
        ans = _θ
        for k in range(_n + 1):
            ans = atan(ans)
    return ans

@lru_cache(maxsize=None)
def acscT(_n , _θ):
    if type(_n)==str:
        k = 0.01
        ans = _θ
        for h in range(len(_n)):
            if _n[h] == "d":
                ans = (acsc(ans + k) - acsc(ans)) / k
            else:
                raise Exception('The value of the argument must be a string that contains only "d" or a natural number.')
        return ans
    elif _n <= 0 or not _n % 1 == 0:
        raise Exception('The value of the argument must be a string that contains only "d" or a natural number.')
    else:
        ans = _θ
        for k in range(_n + 1):
            ans = acsc(ans)
    return ans

@lru_cache(maxsize=None)
def asecT(_n , _θ):
    if type(_n)==str:
        k = 0.01
        ans = _θ
        for h in range(len(_n)):
            if _n[h] == "d":
                ans = (asec(ans + k) - asec(ans)) / k
            else:
                raise Exception('The value of the argument must be a string that contains only "d" or a natural number.')
        return ans
    elif _n <= 0 or not _n % 1 == 0:
        raise Exception('The value of the argument must be a string that contains only "d" or a natural number.')
    else:
        ans = _θ
        for k in range(_n + 1):
            ans = asec(ans)
    return ans

@lru_cache(maxsize=None)
def acotT(_n , _θ):
    if type(_n)==str:
        k = 0.01
        ans = _θ
        for h in range(len(_n)):
            if _n[h] == "d":
                ans = (acot(ans + k) - acot(ans)) / k
            else:
                raise Exception('The value of the argument must be a string that contains only "d" or a natural number.')
        return ans
    elif _n <= 0 or not _n % 1 == 0:
        raise Exception('The value of the argument must be a string that contains only "d" or a natural number.')
    else:
        ans = _θ
        for k in range(_n + 1):
            ans = acot(ans)
    return ans

@lru_cache(maxsize=None)
def sinhT(_n , _θ):
    if type(_n)==str:
        k = 0.01
        ans = _θ
        for h in range(len(_n)):
            if _n[h] == "d":
                ans = (sinh(ans + k) - sinh(ans)) / k
            else:
                raise Exception('The value of the argument must be a string that contains only "d" or a natural number.')
        return ans
    elif _n <= 0 or not _n % 1 == 0:
        raise Exception('The value of the argument must be a string that contains only "d" or a natural number.')
    else:
        ans = _θ
        for k in range(_n + 1):
            ans = sinh(ans)
    return ans

@lru_cache(maxsize=None)
def coshT(_n , _θ):
    if type(_n)==str:
        k = 0.01
        ans = _θ
        for h in range(len(_n)):
            if _n[h] == "d":
                ans = (cosh(ans + k) - cosh(ans)) / k
            else:
                raise Exception('The value of the argument must be a string that contains only "d" or a natural number.')
        return ans
    elif _n <= 0 or not _n % 1 == 0:
        raise Exception('The value of the argument must be a string that contains only "d" or a natural number.')
    else:
        ans = _θ
        for k in range(_n + 1):
            ans = cosh(ans)
    return ans

@lru_cache(maxsize=None)
def tanhT(_n , _θ):
    if type(_n)==str:
        k = 0.01
        ans = _θ
        for h in range(len(_n)):
            if _n[h] == "d":
                ans = (tanh(ans + k) - tanh(ans)) / k
            else:
                raise Exception('The value of the argument must be a string that contains only "d" or a natural number.')
        return ans
    elif _n <= 0 or not _n % 1 == 0:
        raise Exception('The value of the argument must be a string that contains only "d" or a natural number.')
    else:
        ans = _θ
        for k in range(_n + 1):
            ans = tanh(ans)
    return ans

@lru_cache(maxsize=None)
def cschT(_n , _θ):
    if type(_n)==str:
        k = 0.01
        ans = _θ
        for h in range(len(_n)):
            if _n[h] == "d":
                ans = (csch(ans + k) - csch(ans)) / k
            else:
                raise Exception('The value of the argument must be a string that contains only "d" or a natural number.')
        return ans
    elif _n <= 0 or not _n % 1 == 0:
        raise Exception('The value of the argument must be a string that contains only "d" or a natural number.')
    else:
        ans = _θ
        for k in range(_n + 1):
            ans = csch(ans)
    return ans

@lru_cache(maxsize=None)
def sechT(_n , _θ):
    if type(_n)==str:
        k = 0.01
        ans = _θ
        for h in range(len(_n)):
            if _n[h] == "d":
                ans = (sech(ans + k) - sech(ans)) / k
            else:
                raise Exception('The value of the argument must be a string that contains only "d" or a natural number.')
        return ans
    elif _n <= 0 or not _n % 1 == 0:
        raise Exception('The value of the argument must be a string that contains only "d" or a natural number.')
    else:
        ans = _θ
        for k in range(_n + 1):
            ans = sech(ans)
    return ans

@lru_cache(maxsize=None)
def cothT(_n , _θ):
    if type(_n)==str:
        k = 0.01
        ans = _θ
        for h in range(len(_n)):
            if _n[h] == "d":
                ans = (coth(ans + k) - coth(ans)) / k
            else:
                raise Exception('The value of the argument must be a string that contains only "d" or a natural number.')
        return ans
    elif _n <= 0 or not _n % 1 == 0:
        raise Exception('The value of the argument must be a string that contains only "d" or a natural number.')
    else:
        ans = _θ
        for k in range(_n + 1):
            ans = coth(ans)
    return ans

@lru_cache(maxsize=None)
def asinhT(_n , _θ):
    if type(_n)==str:
        k = 0.01
        ans = _θ
        for h in range(len(_n)):
            if _n[h] == "d":
                ans = (asinh(ans + k) - asinh(ans)) / k
            else:
                raise Exception('The value of the argument must be a string that contains only "d" or a natural number.')
        return ans
    elif _n <= 0 or not _n % 1 == 0:
        raise Exception('The value of the argument must be a string that contains only "d" or a natural number.')
    else:
        ans = _θ
        for k in range(_n + 1):
            ans = asinh(ans)
    return ans

@lru_cache(maxsize=None)
def acoshT(_n , _θ):
    if type(_n)==str:
        k = 0.01
        ans = _θ
        for h in range(len(_n)):
            if _n[h] == "d":
                ans = (acosh(ans + k) - acosh(ans)) / k
            else:
                raise Exception('The value of the argument must be a string that contains only "d" or a natural number.')
        return ans
    elif _n <= 0 or not _n % 1 == 0:
        raise Exception('The value of the argument must be a string that contains only "d" or a natural number.')
    else:
        ans = _θ
        for k in range(_n + 1):
            ans = acosh(ans)
    return ans

@lru_cache(maxsize=None)
def atanhT(_n , _θ):
    if type(_n)==str:
        k = 0.01
        ans = _θ
        for h in range(len(_n)):
            if _n[h] == "d":
                ans = (atanh(ans + k) - atanh(ans)) / k
            else:
                raise Exception('The value of the argument must be a string that contains only "d" or a natural number.')
        return ans
    elif _n <= 0 or not _n % 1 == 0:
        raise Exception('The value of the argument must be a string that contains only "d" or a natural number.')
    else:
        ans = _θ
        for k in range(_n + 1):
            ans = atanh(ans)
    return ans

@lru_cache(maxsize=None)
def acschT(_n , _θ):
    if type(_n)==str:
        k = 0.01
        ans = _θ
        for h in range(len(_n)):
            if _n[h] == "d":
                ans = (acsch(ans + k) - acsch(ans)) / k
            else:
                raise Exception('The value of the argument must be a string that contains only "d" or a natural number.')
        return ans
    elif _n <= 0 or not _n % 1 == 0:
        raise Exception('The value of the argument must be a string that contains only "d" or a natural number.')
    else:
        ans = _θ
        for k in range(_n + 1):
            ans = acsch(ans)
    return ans

@lru_cache(maxsize=None)
def asechT(_n , _θ):
    if type(_n)==str:
        k = 0.01
        ans = _θ
        for h in range(len(_n)):
            if _n[h] == "d":
                ans = (asech(ans + k) - asech(ans)) / k
            else:
                raise Exception('The value of the argument must be a string that contains only "d" or a natural number.')
        return ans
    elif _n <= 0 or not _n % 1 == 0:
        raise Exception('The value of the argument must be a string that contains only "d" or a natural number.')
    else:
        ans = _θ
        for k in range(_n + 1):
            ans = asech(ans)
    return ans

@lru_cache(maxsize=None)
def acothT(_n , _θ):
    if type(_n)==str:
        k = 0.01
        ans = _θ
        for h in range(len(_n)):
            if _n[h] == "d":
                ans = (acoth(ans + k) - acoth(ans)) / k
            else:
                raise Exception('The value of the argument must be a string that contains only "d" or a natural number.')
        return ans
    elif _n <= 0 or not _n % 1 == 0:
        raise Exception('The value of the argument must be a string that contains only "d" or a natural number.')
    else:
        ans = _θ
        for k in range(_n + 1):
            ans = acoth(ans)
    return ans