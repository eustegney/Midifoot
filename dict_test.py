a = {}

zero0 = {0: {'event': 10, 'button': 5}}
zero1 = {0: {'event': 11, 'button': 5}}
zero2 = {0: {'event': 10, 'button': 5}}
zero3 = {0: {'event': 11, 'button': 5}}

one0 = {1: {'event': 10, 'button': 2}}
one1 = {1: {'event': 11, 'button': 2}}

a.update(zero0)
a.update(zero1)
a.update(zero2)
a.update(zero3)
a.update(one0)
a.update(one1)
print(a)