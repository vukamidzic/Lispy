from reader import *
from env import global_env
import os

def eval(expr: Expr, env=global_env) -> Expr:
    # variable reference 
    if isinstance(expr, Symbol):  
        return env[expr]
    # constant number
    elif isinstance(expr, Number):      
        return expr                
    # conditional
    elif expr[0] == 'if': 
        try:              
            (_, test, conseq, alt) = expr # --> (if (test) (expr1) (expr2)) <=> if (test) {expr1} else {expr2}
            exp = (conseq if eval(test, env) else alt)
            return eval(exp, env)
        except Exception:
            return f"Missing or too many arguments"
    # definition
    elif expr[0] == 'def!': # --> (define (symbol) (expr)) <=> symbol = expr  
        try:         
            (_, symbol, exp) = expr
            env[symbol] = eval(exp, env)
        except Exception:
            return f"Missing or too many arguments"
    elif expr[0] == 'set!': # --> (setvar (symbol) (expr)) <=> symbol = expr (if symbol defined earlier)
        try:
            (_, symbol, expr) = expr
            if symbol not in env:
                return f'Uknown var "{symbol}"'
            else:
                env[symbol] = eval(expr, env)
        except Exception:
            return f"Missing or too many arguments"
    elif expr[0] == 'show': # --> (quote (expr)) = "expr" (as string)
        try:
            (_, expr) = expr
            return expr
        except Exception:
            return f"Missing or too many arguments"
    # procedure call
    else: 
        try:                           
            proc = eval(expr[0], env)
            args = [eval(arg, env) for arg in expr[1:]]
            return proc(*args)
        except Exception as e:
            return e

def lispstr(expr):
    if isinstance(expr, List):
        return '(' + ' '.join(map(lispstr, expr)) + ')'
    else:
        return str(expr)

def repl(prompt='lispy> '): 
    print('Read-eval-print loop')
    while True:
        cmd = input(prompt)
        if cmd == 'q':
            break
        elif cmd == 'clean':
            os.system('cls')
        else:
            val = eval(parse(cmd), global_env)
            if val is not None:
                print(lispstr(val))
    
repl()