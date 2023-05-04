from reader import (Env, Number, Symbol)

import math 
import operator as op

def std_env() -> Env:
    env = Env()
    # mapping function names into their definitions
    env.update(vars(math)) 
    env.update({
        'abs': abs,
        'pow': math.pow,
        '+': op.add,
        '-': op.sub,
        '*': op.mul,
        '/': op.truediv,
        '>': op.gt,
        '<': op.lt,
        '>=': op.ge,
        '<=': op.le,
        '=': op.eq,
        '~=': op.ne,
        'eval': lambda *x: x[-1],
        'num?': lambda x: isinstance(x, Number),
        'sym?': lambda x: isinstance(x, Symbol),
    })
    return env

global_env = std_env()