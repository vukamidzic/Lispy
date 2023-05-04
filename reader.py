# Type definitions 
Symbol = str
Number = (int, float) # either integer or float
Atom = (Symbol, Number) # atom is either a variable or a number
List = list 
Expr = (Atom, List) # expr is defined as single expression or list of them
Env = dict # dictionary where we keep track of variables

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