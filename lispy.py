# Type definitions 
Symbol = str
Number = (int, float) # either integer or float
Atom = (Symbol, Number) # atom is either a variable or a number
List = list 
Expr = (Atom, List) # expr is defined as single expression or list of them

def tokenize (expr: str) -> list:
    return expr.replace('(', ' ( ').replace(')', ' ) ').split()

def parse(program: str) -> Expr:
    return read_tokens(tokenize(program))

def atom(token: str) -> Atom:
    try: return int(token)
    except ValueError:
        try: return float(token)
        except ValueError:
            return Symbol(token)

def read_tokens(tokens: list) -> Expr:
    if len(tokens) == 0:
        raise SyntaxError('Unexpected EOF')
    token = tokens.pop(0)
    if token == '(':
        # ( elems ) ==> [elems] without a ')'
        L = []
        while tokens[0] != ')':
            L.append(read_tokens(tokens))
        tokens.pop(0)
        return L
    elif token == ')':
        raise SyntaxError('Unexpected '')'' ')
    else:
        return atom(token)

import math 
import operator as op
import os

class Env(dict):
    def __init__(self, params=(), args=(), outer = None):
        self.update(zip(params, args))
        self.outer = outer
    def find(self, var):
        return self if (var in self) else self.outer.find(var)

def std_env():
    env = Env()
    # mapping function names into their definitions
    env.update(vars(math)) 
    env.update({
        'abs': abs,
        'pow': math.pow,
        'round': round,
        '+': op.add,
        '-': op.sub,
        '*': op.mul,
        '/': op.truediv,
        '<<': op.lshift,
        '>>': op.rshift,
        '>': op.gt,
        '<': op.lt,
        '>=': op.ge,
        '<=': op.le,
        '=': op.eq,
        'not': op.not_,
        'and': op.and_,
        'or': op.or_,
        'eq?': op.is_,
        '~=': op.ne,
        'max': max,
        'max': min,
        'list': lambda *x: List(x),
        'fst': lambda x: x[0],
        'rst': lambda x: x[1:],
        'cons': lambda x, y: [x] + y,
        'map': lambda f, ls: list(map(f, ls)),
        'filter': lambda f, ls: list(filter(f, ls)),
        'len': lambda x: len(x), 
        'print': print,
        'num?': lambda x: isinstance(x, Number),
        'sym?': lambda x: isinstance(x, Symbol),
        'list?': lambda x: isinstance(x, List),
        'proc?': lambda x: isinstance(x, Proc),
        'null?': lambda x: x == []
    })
    return env

class Proc(object):
    def __init__(self, params, body, env):
        self.params, self.body, self.env = params, body, env
    def __call__(self, *args): 
        return eval(self.body, Env(self.params, args, self.env))

global_env = std_env()

def eval(expr: Expr, env = global_env) -> Expr:
    if isinstance(expr, Symbol):
        return env.find(expr)[expr]
    elif not isinstance(expr, List):
        return expr
    
    op, *args = expr

    if op == 'show':
        return args[0]
    elif op == 'if':
        (test, conseq, alt) = args
        expr = (conseq if eval(test, env) else alt)
        return eval(expr, env)
    elif op == 'def!': 
        (symbol, expr) = args
        env[symbol] = eval(expr, env)
    elif op == 'set!':
        (symbol, expr) = args
        env.find(symbol)[symbol] = eval(expr, env)
    elif op == 'lambda':         
        (params, body) = args
        return Proc(params, body, env)
    else:
        proc = eval(op, env)
        vals = [eval(arg, env) for arg in args]
        return proc(*vals)

def lispstr(expr):
    if isinstance(expr, List):
        return '(' + ' '.join(map(lispstr, expr)) + ')'
    else:
        return str(expr)

def repl(prompt='lispy> '): 
    while True:
        expr = input(prompt)
        if expr == 'quit':
            break
        elif expr == 'clean':
            os.system('cls')
        else:
            val = eval(parse(expr))
            if val is not None: 
                print(lispstr(val))
    
repl()