# Lispy

Simple intepreter for Lisp expressions with basic arithmetic, logical and list operations in Python. 

## About
Lispy, like the original Lisp, represents functional paradigm and it consists of list of expressions written in parentheses. 
Basic forms in Lispy are:
-  variable references (example: r => 10, assuming that r was defined as 10)
-  constants (in Lispy, those are numbers (int or float); example: 12 => 12, 3.45e3 => 3.45e3)
-  conditionals (syntax: (if (cond) (expr1) (expr2)), equivalent to if (cond) {stmts1} else {stmts2} in C. Example:  (if (< 2 1) (+ 1 1) (+ 2 2)) => 4)
-  definitions (syntax: (def! var expr); they define a new variable and assign in a value. Example: (def! r 10) is equal to writing int r = 10; in C )
-  assignments (syntax: (set! var expr); like definitions but can assign only to predefined variables.)
-  procedures (syntax: (proc args) or (lambda (params) (body)); in first case the proc is applied to arguments, while in second case, the body is being executed with the given parameters. Example: (def! square (lambda (n) (* n n)))
-  lists (defined as (list [elems]); example: (list 1 2 3) --> [1,2,3], (list) --> [])

## Examples

```
lispy> (+ 2 2)
4
lispy> (def! n 10)
lispy> (if (= n 10) (+ n 1) (/ n 2))
11
lispy> (def! fact (lambda (n) (if (<= n 1) 1 (* n (fact (- n 1))))))
lispy> (fact 5)
120
lispy> (def! f (lambda (n) (+ n 1)))
lispy> (map f (list 1 2 3))
(2 3 4)
```

## Running the REPL
To run it, type
```
python3 lispy.py
```
Currently there are only commands ```quit``` for exiting the REPL and ```clean``` to clear previous lines.
(It is necessary to have Python version 3.9 or later).
