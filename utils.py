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
    partie_gauche0 = a[0:l]
    retenue, partie_droite = add_one(a[l:size])
    ret_1, partie_gauche1 = add_one(partie_gauche0)
    return retenue & ret_1, Mux(retenue, partie_gauche0, partie_gauche1) + partie_droite

def sign_extend(target:int, value: Variable, enable: Variable) -> Variable:
    '''Sign extend'''
    s = Mux(enable, Constant("0"), value[0])
    res = value
    for i in range(value.bus_size, target):
        res = s + res
    return res

def multimux(choice:Variable, vars:list[Variable]) -> Variable:
    '''This multiplexer is lazy and will not return an error if the provided list
    and choice are incompatible. However, it supports multiplexer with (not a power
    of 2) entries. It selects the entry by its index in the provided list.'''
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
        multimux(new_choice, [vars[i] for i in range(0, size, 2)]),
        multimux(new_choice, [vars[i] for i in range(1, size, 2)])
    )
