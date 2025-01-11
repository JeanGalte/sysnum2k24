from lib_carotte import *

def add_one(a:Variable) -> (Variable, Variable):
    '''renvoie un booleen generate et le resultat'''
    size = a.bus_size
    if size == 0:
        return Constant("1"), Constant("")
    if size == 1:
        return a, ~a
    l = size//2
    r = size - l
    partie_droite0 = a[l:size]
    ret_0, partie_droite1 = add_one(partie_droite0)
    retenue, partie_gauche = add_one(a[0:l])
    return retenue & ret_0, partie_gauche + Mux(retenue, partie_droite0, partie_droite1)

def sign_extend(target:int, value: Variable, enable: Variable) -> Variable:
    '''Sign extend'''
    s = Mux(enable, Constant("0"), value[value.bus_size-1])
    res = value
    for i in range(value.bus_size, target):
        res = res + s
    return res

def multimux(choice:Variable, vars:list[Variable]) -> Variable:
    '''This multiplexer is lazy and will not return an error if the provided list
    and choice are incompatible. However, it supports multiplexer with (not a power
    of 2) entries. It selects the entry by its index in the provided list
    (little endian).'''
    size = len(vars)
    bw = choice.bus_size
    if size == 0:
        raise Exception("Cannot choose from no value.")
    if size == 1:
        return vars[0]
    if size == 2:
        if bw == 1:
            choice_bis = choice
        else:
            choice_bis = choice[0]
        return Mux(choice_bis, vars[0], vars[1])
    new_choice = choice[1:bw]
    return Mux(choice[0],
        multimux(new_choice, [vars[i] for i in range(0, size, 2)]),
        multimux(new_choice, [vars[i] for i in range(1, size, 2)])
    )

def multimux_be(choice:Variable, vars:list[Variable]) -> Variable:
    '''This multiplexer is lazy and will not return an error if the provided list
    and choice are incompatible. However, it supports multiplexer with (not a power
    of 2) entries. It selects the entry by its index in the provided list
    (big endian).'''
    size = len(vars)
    bw = choice.bus_size
    if size == 0:
        raise Exception("Cannot choose from no value.")
    if size == 1:
        return vars[0]
    if size == 2:
        if bw == 1:
            choice_bis = choice
        else:
            choice_bis = choice[bw-1]
        return Mux(choice_bis, vars[0], vars[1])
    new_choice = choice[0:bw-1]
    return Mux(choice[bw-1],
        multimux_be(new_choice, [vars[i] for i in range(0, size, 2)]),
        multimux_be(new_choice, [vars[i] for i in range(1, size, 2)])
    )

def is_not_null(a:Variable) -> Variable:
    n = a.bus_size
    if n==1:
        return a
    return is_not_null(a[0:n//2]) | is_not_null(a[n//2:n])
