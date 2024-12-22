from lib_carotte import *

def mux4(choice:Variable, v00:Variable, v01:Variable, v10:Variable, v11:Variable) -> Variable:
    c = Select(1, choice)
    return Mux(Select(0, choice), Mux(c, v00, v01), Mux(c, v10, v11))
def mux8(choice:Variable, v000:Variable, v001:Variable, v010:Variable, v011:Variable,
                          v100:Variable, v101:Variable, v110:Variable, v111:Variable) -> Variable:
    c2 = Slice(1, 3, choice)
    return Mux(Select(0, choice),
               mux4(v000, v001, v010, v011, c2),
               mux4(v100, v101, v110, v111, c2))

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
