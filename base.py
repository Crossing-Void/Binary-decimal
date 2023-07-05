from traceback import format_exc
from abc import ABC, abstractclassmethod
import re
import sys


__all__ = ['Binary', 'Decimal']


def debug(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as err:
            err_line = re.findall('(line\s*\d+)', format_exc())
            print(*err_line, f'\n{err.__class__.__name__}, {err}')
            sys.exit()
    return inner


class Number(ABC):
    @debug
    def __init__(self, number: str):
        if type(number) != str:
            raise TypeError(
                f'The parameter number should be str, but get a {type(number)}'
            )
        number = number.strip()
        if not(number):
            raise ValueError('Not support empty number')
        if number in ('.', '-', '-.'):
            raise ValueError(
                f'The {number} is not valid for the base: {self.base}')
        match = re.fullmatch(
            '(?P<sign>-)?' +
            '(?P<intPart>' + self.getcipher() + '*)' +
            '(?P<point>\.?)' +
            '(?P<floatPart>' + self.getcipher() + '*)', number)
        if match:
            self.sign = match.group('sign')
            self.intPart = match.group('intPart')
            self.floatPart = match.group('floatPart')
            self.point = match.group('point')
        else:
            raise ValueError(
                f'The {number} is not valid for the base: {self.base}')

    @debug
    def getnumber(self):
        intPart = '0' if not(
            self.intPart) and self.point and self.floatPart else self.intPart
        floatPart = '0' if not(
            self.floatPart) and self.intPart and self.point else self.floatPart
        try:
            return self.sign + intPart + self.point + floatPart
        except:
            return intPart + self.point + floatPart

    @debug
    def getcipher(self):
        if self.base > 36:
            raise ValueError(
                'Greater than 36 base is not supported: {self.base}')
        return '[' + ''.join([chr(x) for x in range(48, 48+self.base if self.base < 11 else 58)] +
                             [chr(x) for x in range(97, 97+self.base-10)]) + ']'

    @abstractclassmethod
    def __add__(self, value):
        pass

    @abstractclassmethod
    def __mul__(self, value):
        pass

    @abstractclassmethod
    def __sub__(self, value):
        pass

    @abstractclassmethod
    def __truediv__(self, value):
        pass

    @abstractclassmethod
    def __floordiv__(self, value):
        pass

    @abstractclassmethod
    def __mod__(self, value):
        pass

    @abstractclassmethod
    def __pow__(self, value):
        pass

    @debug
    def __str__(self):
        return f'<{self.__class__.__name__} object number: {self.getnumber()}, base: {self.base}>'

    @debug
    def __repr__(self):
        return f'<{self.__class__.__name__} object number: {self.getnumber()}, base: {self.base}>'


class Binary(Number):
    base = 2

    def __init__(self, number):
        super().__init__(number)

    @debug
    def __operate(self, value, operate):
        if type(value) != self.__class__:
            raise TypeError(
                f'{self.__class__.__name__} and {value.__class__.__name__} can not do addition')

        num1 = self.change_to_10()
        num2 = value.change_to_10()
        return Decimal(eval(f'num1 {operate} num2').getnumber()).change_to_2()

    def __add__(self, value):
        return self.__operate(value, '+')

    def __mul__(self, value):
        return self.__operate(value, '*')

    def __sub__(self, value):
        return self.__operate(value, '-')

    def __truediv__(self, value):
        return self.__operate(value, '/')

    def __floordiv__(self, value):
        return self.__operate(value, '//')

    def __mod__(self, value):
        return self.__operate(value, '%')

    def __pow__(self, value):
        return self.__operate(value, '**')

    @debug
    def change_to_10(self):
        result = 0
        #int part#
        for digit, power in zip(self.intPart[::-1], range(len(self.intPart))):
            if int(digit):
                result += 2 ** power
        #int part#
        #float part#
        for digit, power in zip(self.floatPart, range(-1, -len(self.floatPart)-1, -1)):
            if int(digit):
                result += 2 ** power
        #float part#
        try:
            return Decimal(self.sign + str(result) + ('.0' if type(result) == int and self.point else ''))
        except:
            return Decimal(str(result) + ('.0' if type(result) == int and self.point else ''))


class Decimal(Number):
    base = 10

    def __init__(self, number):
        super().__init__(number)

    @debug
    def __operate(self, value, operate):
        if type(value) != self.__class__:
            raise TypeError(
                f'{self.__class__.__name__} and {value.__class__.__name__} can not do addition')

        num1 = float(self.getnumber()) if self.point else int(
            self.getnumber())
        num2 = float(value.getnumber()) if value.point else int(
            value.getnumber())
        return self.__class__(str(eval(f'num1 {operate} num2')))

    def __add__(self, value):
        return self.__operate(value, '+')

    def __mul__(self, value):
        return self.__operate(value, '*')

    def __sub__(self, value):
        return self.__operate(value, '-')

    def __truediv__(self, value):
        return self.__operate(value, '/')

    def __floordiv__(self, value):
        return self.__operate(value, '//')

    def __mod__(self, value):
        return self.__operate(value, '%')

    def __pow__(self, value):
        return self.__operate(value, '**')

    @debug
    def change_to_2(self):
        #int Part#
        initial_int = int(self.intPart) if self.intPart else 0
        remainder_int = []
        while initial_int != 0:
            initial_int, remain = divmod(initial_int, 2)
            remainder_int.append(str(remain))
        #int Part#
        #float part#
        initial_float = int(self.floatPart) if self.floatPart else 0
        remainder_float = []
        for _ in range(32):
            if initial_float == 0:
                break
            initial_float *= 2
            if initial_float >= 10 ** len(self.floatPart):
                initial_float -= 10 ** len(self.floatPart)
                remainder_float.append('1')
            else:
                remainder_float.append('0')

        #float part#
        result_int = ''.join(remainder_int[::-1]) if remainder_int else '0'
        result_float = ''.join(remainder_float) if remainder_float else (
            '0' if self.point else '')
        try:
            return Binary(self.sign + result_int + self.point + result_float)
        except:
            return Binary(result_int + self.point + result_float)


if __name__ == '__main__':
    num = Binary('110.01')
    print((num % Binary('110.001')).change_to_10())
