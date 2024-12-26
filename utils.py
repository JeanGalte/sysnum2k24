from lib_carotte import *

def add_one(size:int, a:Variable):
    '''renvoie un booleen generate et le resultat'''
    if size == 0:
        return Constant("1"), Constant("")
    if size == 1:
        return a, Not(a)
    l = size//2
    r = size - l
    partie_gauche0 = Slice(0, l, a)
    retenue, partie_droite = add_one(r, Slice(l, size, a))
    ret_1, partie_gauche1 = add_one(l, partie_gauche0)
    return And(retenue, ret_1), Concat(Mux(retenue, partie_gauche0, partie_gauche1), partie_droite)

def multimux(choice:Variable, vars:list[Variable]):
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
            choice_bis = Select(bw-1, choice)
        return Mux(choice_bis, vars[0], vars[1])
    new_choice = Slice(0, bw-1, choice)
    return Mux(Select(bw-1, choice),
        multimux(new_choice, [vars[i] for i in range(0, size, 2)]),
        multimux(new_choice, [vars[i] for i in range(1, size, 2)])
    )
