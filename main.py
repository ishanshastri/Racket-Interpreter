import numpy as np
import  math
import ast
'''
def extract_elements(expr):
    lst = expr.split()
    operator = lst[0][1]
    args_list = []

    for arg in lst[1:]:
        if '(' in arg:
            end = arg.find(')') #Error handle if -1
            print(arg)
            args_list.append(arg[1, end])
        else:
            args_list.append(arg)

    #args_list = lst[1:len(lst)]
    return (operator, np.array(args_list))

#intersecting splits ( and ) 
def extract_elements2(expr):
    opbr = expr.split('(')
    clbr = expr.split(')')
    #print(opbr)
    #print(clbr)

    #for e in expr:

    
def evaluate_exp(exp):
    exp_stack = []
    for i in range(len(exp)):
        if exp[i]=='(':
            exp_stack.append(evaluate_exp(exp[i: exp.find(')')]))
            i = exp.find(')')
        else:
            exp_stack.append(exp[i])
    if '(' not in exp: # If base value then just return
        return exp

    #Get operator and arguments (if not a base value)
    #exp_tup = extract_elements(exp)
    #op = exp_tup[0]
    #args = exp_tup[1]

    #cases
    if op=="+":
        func = lambda a, b: a+b
    if op=="-":
        func = lambda a, b: a-b
    if op=="*":
        func = lambda a, b: a*b
    if op=="/": 
        func = lambda a, b: a/b

    #for v in args:

def eval_expp(expr):
    if '(' not in expr: # If base value then just return
        return expr

    exp_stack = []
    for i in range(len(expr)):
        if expr[i]=='(':
            exp_stack += (eval_expp(expr[i: expr.find(')')]))
            i = expr.find(')')
        elif expr[i]!="" and expr[i]!=" ":
            exp_stack.append(expr[i])
        #print(expr[i])
    return exp_stack

def eval_arithmetic(val1, val2, op):
    return ''

def eval_exp(expr):
    if '(' not in expr: # If base value then just return
        return expr


def extr_exp_2(rexp):
    lst = expr.split()
    operator = lst[1]
    args_list = []
    rest = lst[1:-1]
    inbrac = False
    for i in range(len(rest)):
        print(i)
        if rest[i] == '(':
            inbrac = True
            continue
        if inbrac:
            indof = rest.index(')')+1
            args_list.append(' '.join(rest[i:indof]))
            
        elif rest[i] != ')':
            args_list.append(rest[i])
    return (operator, args_list)
'''
functions = {}#funcs

#Elementry ops:
'''
functions['+'] = lambda a, b: a+b
functions['-'] = lambda a, b: a-b
functions['*'] = lambda a, b: a*b
functions['/'] = lambda a, b: a/b
functions['expt'] = lambda a, b: a**b
functions['abs'] = lambda a: abs(a)
functions['&'] = lambda a:a
'''
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
    #curind = exp.find('(')
    #while curind != -1:
        #if exp[curind+1]!=' ':
    #return exp.split()

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

    #cases
    '''
    func = lambda a:a
    if op=='+':
        func = lambda a, b: a+b
    if op=='-':
        func = lambda a, b: a-b
    if op=='*':
        func = lambda a, b: a*b
    if op=='/': 
        func = lambda a, b: a/b
    '''
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
'''
def extr_body(rbody):
    return ""
'''
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
#print(get_func_body("(define (f x y z) (* z (+ x y)))"))
'''
def repl(s, params, args):
    print(params)
    for i in range(len(params)):
        s = s.replace(params[i], args[i])

def repl(exp, param, arg):
    return exp.replace(param, arg)

def sub_val(expr, args):
    """args must be in correct order, args are chars"""
    body = get_func_body(expr)
    params = get_func_def(expr)[1]
    dumargs = np.array(body[1]) #dummy arguments (eg. x, y, z)
    rep = np.vectorize(repl, excluded=[0])#str.replace)
    #vectorize and replace all occurences of vars with respective values; then send to be evaluated!
    
    #print(dumargs)
    #subbed_exp = rep(dumargs, params, args)
    
    print(get_raw_body(expr))
    subbed_exp = rep(get_raw_body(expr), params, args)
    #for e in dumargs:
    #    e.rep(args[np.where(dumargs == e)])
    return subbed_exp
'''
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
'''
def petvalu_expr(expr):
    expr = get_func_body(expr)
    return expr

def add_func(rfunc):
    defn = get_func_def(rfunc)
    lamb_expr = ""
    for p in defn[1]:
        lamb_expr += 'lambda ' + p + ': ' 
    return lamb_expr#STUB
#print(add_func("( define ( f x y z ) ( ... ) )"))

def spcomm():
    """A function desgined to generate pain"""
    return
'''

expr = "(+ 9 0 9 (- 9 8 ) (* 2 4 (- 8 9 ) (/ 7 6)))"
#print(petvalu_expr("(define (f x y z) (* z (+ x y)))"))
#run(expr) #input string from file
#print(preprocess(expr))

'''
exec('print("Yo")')
exec("""inc = lambda x:x+1
functions['inc'] = inc""")
print(functions['inc'](2))
'''

'''
print(eval_expr_lambda(expr))
#print(extr_expr(expr))
#print(eval_expr(expr))
print(eval_expr_lambda("(abs -8)"))
#print((preprocess(expr)))

x = lambda a: (lambda b: a + b)
#print(x(x(7)(8))(9))
#print(x(3)(4))


sus = lambda u: (lambda a: u + [a])
lsd = []
#print(sus(sus(lsd)('o'))('p'))
circle = lambda a: (lambda x: math.sqrt(a**2 + x**2))
#print(circle(3)(3))
sphere = lambda x: (lambda y: (lambda z: math.sqrt(x**2 + y**2 + z**2)))
#print(sphere(1)(1)(1))
#print(sphere(sphere(1))(5))
'''
#fac = lambda n : 1 if n == 0 else n * fac(n-1)
#print(fac(5))
