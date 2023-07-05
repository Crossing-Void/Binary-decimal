# bin_decimal

## Preface

This is a modules for different number base numbers to interchage  
the default class Binary and Decimal already built, and you can expand 
other class like Octal etc. (limit is 36)

# Modules

## base.py

> The function is so many that using example to illustrate  
> create object: `num = Binary("110.011")`
> print object: `print(num)`
> get the numbers part: `print(num.sign, num.intPart, num.floatPart, num.point)`
> get the letter or number use in the system: `print(num.getcipher())`
> return a string represent the value of number: `print(num.getnumber())`
> get the base: `print(num.base)`
> change binary to decimal: `print(num.change_to_10())`
> do some arithmetics: `Binary("110.011") + Binary("100.110")`  
also -, *, /, //, %, ** 