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

#list functions
functions['cons'] = lambda a: (lambda b: [a] + b)
functions['append'] = lambda a: (lambda b: b + [a])
functions['list'] = lambda a: (lambda b: (a if(isinstance(a, list)) else [a]) + [b])
functions['first'] = lambda l: l[0]
functions['second'] = lambda l: functions['first'](functions['rest'](l)) 
functions['rest'] = lambda l: l[1:]
#functions['append'] = functions['list']
#Bool Funcs
functions['if'] = lambda a: (lambda b: (lambda c: b if(a) else c))#__freeze(not(a), c)))
functions['or'] = lambda a: (lambda b: a or b)
functions['and'] = lambda a: (lambda b: a and b)
functions['='] = lambda a: (lambda b: (a==b))
functions['Y'] = lambda f: lambda x: f(Y(f))(x)#lambda f: (lambda x: f())
#def new_function(rfunc):
    
#Complicated Funcsions#
#def __cond_()

def __freeze(flag, val):
    if flag:
        val
    else:
        0

def validate(exp):
    #STUB-TODO
    return True

def is_function(val):
    return isinstance(val, type(lambda x:1))

def preprocess(exp):
    #add spaces where necc
    result = []
    #exp = exp.replace("true", "lambda x: (lambda y: x)")
    #exp = exp.replace("false", "lambda x: (lambda y: y)")
    #print(exp)
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
        if exp=="true":
            return True
        elif exp=="false":
            return False
        else:
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
    """args must be in correct order, args are chars; expr is the raw string function defn."""
    params = get_func_def(expr)[1]
    #print(expr)
    #print(get_func_def(expr)[0])
    if get_func_def(expr)[0] in get_raw_body(expr):
        print("recursive")
    subbed_exp = repl(get_raw_body(expr), params, args)
    #print(subbed_exp)
    return subbed_exp

#print(sub_val("(define (f x y z) (* z (+ x y)))", ['1', '1', '5']))
Y = lambda f: lambda x: f(Y(f))(x)
def add_func(rfunc):
    defn = get_func_def(rfunc)
    lamb_expr = 'functions[get_func_def(rfunc)[0]] = '

    lam_ext = ''
    for p in defn[1]:
        lamb_expr += 'lambda ' + p + ': ' 
        lam_ext +=  'lambda ' + p + ': ' 

    args = get_func_def(rfunc)[1].copy()


    # F = lambda fac: (lambda n: eval_expr(sub_val(n, fac)))
    #functions['fac'] = lambda n: Y(F)(n)
    #functions['fac'] = lambda n: Y( lambda fac: (lambda n: eval_expr(sub_val(n, fac))) )(n)

    #print(lamb_expr)
    #print(str(ast.literal_eval(args)))
    stringify = np.vectorize(str)
    #print(str(stringify(np.array(args)).ravel()))
    #print(args)
    stringified_args = "["
    for a in args:
        stringified_args+= a + ", "
    stringified_args = stringified_args[0:-2] 
    stringified_args += "]"

    #Handle recursive functions
    #F = 'lambda ' + get_func_def(rfunc)[0] + ':' + lam_ext + 'eval_expr_lambda(sub_val(\"' + rfunc + '\", ' +  stringified_args + '))'
    curried_args = ''
    for a in args:
        curried_args += '(' + a + ')'
    F = 'lambda ' + get_func_def(rfunc)[0] + ':' + lam_ext + get_func_def(rfunc)[0] + curried_args
    if (get_func_def(rfunc)[0]=="fac"):#stub
        lamb_expr += 'Y(' + F + ')'
        for a in args:
            lamb_expr += '(' + a + ')'
        print(lamb_expr)
        exec(lamb_expr)
        return functions
        #return 

    #print(stringified_args)
    #lamb_expr += 'eval_expr_lambda(sub_val(\"' + rfunc + '\", ' +  str(stringify(np.array(args)).ravel()) + '))'
    lamb_expr += 'eval_expr_lambda(sub_val(\"' + rfunc + '\", ' +  stringified_args + '))'
    print(lamb_expr)
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

add_func("(define (fac n) (if (= n 1) 1 (* n (fac (- n 1)))))")
print(eval_expr_lambda("(fac 5)"))

#add_func("(define (facc n) (Y fac))")
#print(functions['fac'])
#print(eval_expr_lambda("(Y fac)"))
#expi = lambda x: lambda y: lambda z: eval_expr_lambda(sub_val("(define (f x y z) (* z (+ x y)))", [x, y, z]))
#print("Example: ", expi('1')('2')('2'))
#print(eval_expr_lambda("()"))
expr = "(+ 9 0 9 (f (- (f 2 1 1) 1) 1 1) (- 9 8 ) (* 2 4 (- 8 9 ) (/ 7 6)))"
print(eval_expr_lambda(expr))
print(eval_expr_lambda("(second (list 1 3 4 (cons -1 (append 6 (list 2 4 2)))))"))
#print(eval_expr_lambda("(true 9 8)"))
#print(petvalu_expr("(define (f x y z) (* z (+ x y)))"))
#run(expr) #input string from file
#print(preprocess(expr))

#fac = lambda n : 1 if n == 0 else n * fac(n-1)
#print(fac(5))
print(eval_expr_lambda("(if (= 4 4) 9   ( if    (= 4 4)  2  3) )"))#Testing variability of whitespacing
print(eval_expr_lambda("(= 4 4)"))
iff = lambda a: (lambda b: (lambda c: b if(a) else c))
#print(iff(False)(2)("idk"))

#Y = lambda f: (lambda x: f(f(x)))(lambda x: f(f(x)))
Y = lambda f: lambda x: f(Y(f))(x)
F = lambda f: (lambda n: 1 if(n==0) else (n*f(n-1)))

# F = lambda fac: (lambda n: eval_expr(sub_val(n, fac)))
#functions['fac'] = lambda n: Y(F)(n)
#functions['fac'] = lambda n: Y( lambda fac: (lambda n: eval_expr(sub_val(n, fac))) )(n)

    
#print(F(Y(F))(3))
print(F(F(F(F(F(F(F(F(F(F)))))))))(6)) #Without the y-combinator
print(Y(F)(9)) #Using the y-combinator
'''
def fac(f, n):
    t = f
    while True:
        t = f(t(n-1))
    return t
'''
#def f(n):



#print(F(Y(F))(5))
#print(F(Y(F))(5))
#print(F)