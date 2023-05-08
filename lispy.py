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
        'min': min,
        'list': lambda *x: List(x),
        'append': op.add,
        'add': lambda x, y: x + [y],
        'fst': lambda x: x[0],
        'rst': lambda x: x[1:],
        'cons': lambda x, y: [x] + y,
        'map': lambda f, ls: list(map(f, ls)),
        'filter': lambda f, ls: list(filter(f, ls)),
        'len': lambda x: len(x), 
        'write': print,
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

help = '''Help:
    (op expr1 expr2) <==> expr1 op expr2
    where op: + - * / < > <= >= ~= = << >> and not or max min

    (eq? expr1 expr2) --> true if both expr1 and expr2 are identical objects
    example: (eq? 1 1) --> true, (eq? (list 1 2) (list 1 2)) --> false

    (list [elems...]) --> creates a list out of given elements
    example: (list 1 2 3) <--> (1,2,3)

    (append list1 list2) --> appends second list to first
    example: (append (list 1 2 3) (list 4 5 6)) --> (1 2 3 4 5 6)

    (add list [expr|list]) --> adds expression/list as element to a list
    example: (add (list 1 2 3) 4) --> (1 2 3 4), (add (list 1 2 3) (list 1 2 3)) --> (1 2 3 (1 2 3))

    (fst list) --> returns head of list
    example: (fst (list 1 2 3)) --> 1

    (rst list) --> returns everything behind the head of list
    example: (fst (list 1 2 3)) --> (2 3)

    (cons [expr|list] list) --> adds expression/list as element to beginning of list
    example: (cons 4 (list 1 2 3)) --> (4 1 2 3), (cons (list 1 2 3) (list 1 2 3)) --> ((1 2 3) 1 2 3)

    (abs expr) --> returns absolute value of expression
    example: (abs -4) --> 4

    (pow expr power) --> returns power of expression
    example: (pow 2 3) --> 8.0
        
    (round expr) --> returns rounded value of expression
    example: (round 14.5678) --> 15, (round 14.1234) --> 14 

    (map func list) --> maps a list using a function
    example: (def! f (lambda (n) (+ n 1)))
            (map f (list 1 2 3)) --> (2 3 4)

    (filter func list) --> filters a list using a function
    example: (def! f (lambda (n) (> n 2)))
            (filter f (list 1 2 3 4)) --> (3 4)

    (len list) --> returns length of list
    example: (len (list 1 2 3)) --> 3

    (write expr) --> prints value of expression as string
    example: (write (+ 3 4)) --> 7

    (num? expr) --> checks if expression is instance of number
    (sym? expr) --> checks if expression is instance of symbol
    (list? expr) --> checks if expression is instance of list
    (proc? expr) --> checks if expression is instance of lambda procedure
    (null? expr) --> checks if expression is null
    example: (null? 3) --> false, (null? a (a exists)) --> false, (null? (list)) --> true
'''

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
        elif expr == 'help':
            print(help)
        else:
            val = eval(parse(expr))
            if val is not None: 
                print(lispstr(val))
    

repl()