import numpy as np
import  math
import ast

functions = {}#funcs

#Elementry ops:
functions['+'] = lambda a : (lambda b:b+a)
functions['-'] = lambda a: (lambda b:a-b)
functions['*'] = lambda a: (lambda b:b*a)
functions['/'] = lambda a: (lambda b:a/b)
functions['expt'] = lambda a: (lambda b:a**b)
functions['abs'] = lambda a: abs(a)

#def new_function(rfunc):
    

def validate(exp):
    #STUB-TODO
    return True

def is_function(val):
    return isinstance(val, type(lambda x:1))

def preprocess(exp):
    #add spaces where necc
    result = []

    for i in range(len(exp)-1):
        result.append(exp[i])
        if (exp[i+1]==")" and exp[i]!=' ') or (exp[i]=="(" and exp[i]!=' '):
            result.append(' ')
    result.append(exp[-1])
    return ('').join(result).split()

def get_close_index(ind, lst):
    count=0
    for i in range(ind, len(lst)):
        if lst[i]=='(':
            count+=1
        elif lst[i]==')':
            count-=1
        if count==0:
            #print(i)
            return i

def extr_expr(rexp):
    """Note: input is RAW string"""
    lst = preprocess(rexp)
    operator = lst[1]
    args_list = []
    rest = lst[1:-1]
    i = 1
    #print(i)
    #print(rexp)
    while(i < len(rest)):#for i in range(len(rest)):
        #print(i)
        if rest[i] == '(':
            #indof = rest[i:].index(')')+1
            indof = get_close_index(i, rest)#rest.index(')')+1
            args_list.append(' '.join(rest[i:indof+1]))
            #print(rest[i:indof])
            i = indof-1
            #print(rest[i])
            rest[i] = ""
        elif rest[i] != ')':
            args_list.append(rest[i])
        i+=1
    return (operator, args_list)

def eval_expr(exp):
    if '(' not in exp:
        return float(exp)

    exp = extr_expr(exp)
    op = exp[0]
    func = functions[op]
    args = exp[1][1:]
    res = eval_expr(exp[1][0])
    for a in args:
        res = func(res, eval_expr(a))
    if len(args)==0:
        res = func(res)
    return res

def eval_expr_lambda(exp):
    #print(exp)
    if '(' not in exp:
        return float(exp) # Revise for non-numerical cases

    exp = extr_expr(exp)
    op = exp[0]

    func = functions[op]
    args = exp[1][1:]
    res = func(eval_expr_lambda(exp[1][0]))
    for a in args:
        #res = res(a)
        if is_function(res):
            res = res(eval_expr_lambda(a))
        else:
            res = func(res)(eval_expr_lambda(a))
    return res

def run(rkt):
    if not validate(rkt):
        print("Code Monkey")
        return
    print(eval_expr_lambda(rkt))#STUB; only for simple expressions; first extract contants, encode functions, etc.

def get_func_def(rfunc):
    """A tuple consisting of function name (str) and params (Lst[str])"""
    rfunc = preprocess(rfunc)
    def_start = rfunc[1:].index('(')
    def_end = rfunc.index(')')
    defn = rfunc[def_start+2:def_end]
    return (defn[0], defn[1:])
#print(get_func_def("( define ( f x y z ) ( ... ) )"))

def get_raw_body(rfunc):
    return rfunc[rfunc.index(')')+1:-1]

def get_func_body(rfunc):#STUB
    #rfunc = preprocess(rfunc)
    rbody = get_raw_body(rfunc)
    #rbody = 
    expr = extr_expr(rbody)
    
    return expr

def repl(exp, params, args):
    for i in range(len(params)):
        exp = exp.replace(params[i], str(args[i]))
    return exp

def sub_val(expr, args):
    """args must be in correct order, args are chars"""
    params = get_func_def(expr)[1]
    #print(expr)
    subbed_exp = repl(get_raw_body(expr), params, args)
    #print(subbed_exp)
    return subbed_exp

#print(sub_val("(define (f x y z) (* z (+ x y)))", ['1', '1', '5']))

def add_func(rfunc):
    defn = get_func_def(rfunc)
    lamb_expr = 'functions[get_func_def(rfunc)[0]] = '
    for p in defn[1]:
        lamb_expr += 'lambda ' + p + ': ' 
    args = get_func_def(rfunc)[1].copy()
    #print(str(ast.literal_eval(args)))
    stringify = np.vectorize(str)
    #print(str(stringify(np.array(args)).ravel()))
    #print(args)
    stringified_args = "["
    for a in args:
        stringified_args+= a + ", "
    stringified_args = stringified_args[0:-2] 
    stringified_args += "]"
    #print(stringified_args)
    #lamb_expr += 'eval_expr_lambda(sub_val(\"' + rfunc + '\", ' +  str(stringify(np.array(args)).ravel()) + '))'
    lamb_expr += 'eval_expr_lambda(sub_val(\"' + rfunc + '\", ' +  stringified_args + '))'
    #print(rfunc, " d")
    #print(eval_expr_lambda(sub_val("(define (f x y z) (* z (+ x y)))", ['2', '1', '1'])))#make string rep of args
    #print(lamb_expr)
    exec(lamb_expr)
    #functions[get_func_def(rfunc)[0]]
    
    return functions
    #exec()

def add_func_neu(rfunc):
    defn = get_func_def(rfunc)

add_func("(define (f x y z) (* z (+ x y)))")
print(eval_expr_lambda("(f 2 1 1)"))

#expi = lambda x: lambda y: lambda z: eval_expr_lambda(sub_val("(define (f x y z) (* z (+ x y)))", [x, y, z]))
#print("Example: ", expi('1')('2')('2'))

expr = "(+ 9 0 9 (- 9 8 ) (* 2 4 (- 8 9 ) (/ 7 6)))"
#print(petvalu_expr("(define (f x y z) (* z (+ x y)))"))
#run(expr) #input string from file
#print(preprocess(expr))

#fac = lambda n : 1 if n == 0 else n * fac(n-1)
#print(fac(5))
