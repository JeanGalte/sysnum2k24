from lib_carotte import *

def add_one(a:Variable) -> (Variable, Variable):
    '''renvoie un booleen generate et le resultat'''
    size = a.bus_size
    if size == 1:
        return a, ~a
    l = size//2
    r = size - l
    partie_droite0 = a[l:size]
    ret_0, partie_droite1 = add_one(partie_droite0)
    retenue, partie_gauche = add_one(a[0:l])
    return retenue & ret_0, partie_gauche + Mux(retenue, partie_droite0, partie_droite1)

def fast_concat(n:int, a:Variable) -> Variable:
    if n==1:
        return a
    b = fast_concat(n//2, a)
    if n%2:
        return b+b+a
    return b+b

def sign_extend(target:int, value: Variable, enable: Variable) -> Variable:
    '''Sign extend'''
    s = Mux(enable, Constant("0"), value[value.bus_size-1])
    return value + fast_concat(target-value.bus_size, s)

def multimux(choice:list[Variable], vars:list[Variable]) -> Variable:
    '''This multiplexer is lazy and will not return an error if the provided list
    and choice are incompatible. However, it supports multiplexer with (not a power
    of 2) entries. It selects the entry by its index in the provided list
    (little endian).'''
    size = len(vars)
    if size == 0:
        raise Exception("Cannot choose from no value.")
    if size == 1:
        return vars[0]
    if size == 2:
        return Mux(choice[0], vars[0], vars[1])
    new_choice = choice[1:]
    return Mux(choice[0],
        multimux(new_choice, [vars[i] for i in range(0, size, 2)]),
        multimux(new_choice, [vars[i] for i in range(1, size, 2)])
    )

def is_not_null(a:list[Variable]) -> Variable:
    n = len(a)
    if n==1:
        return a[0]
    return is_not_null(a[0:n//2]) | is_not_null(a[n//2:n])
