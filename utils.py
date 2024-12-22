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

def main():
    overflow, a = add_one(6, Constant("100110"))
    a.set_as_output("a")