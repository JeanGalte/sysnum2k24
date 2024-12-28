from lib_carotte import *

def eq(a, b):
    c = Xor(a, b)
    return Not(c)

def eq_const(a, n):
    one = Constant("1")
    zero = Constant("0")
    c = None
    for i in range(5):
        b = a[i]
        d = eq(b, one if (n >> i) & 1 else zero)
        if c is None:
            c = d
        else:
            c = And(c, d)
    return c

def or_reduce(a):
    if len(a) == 1:
        return a[0]
    return or_reduce(a[:len(a)//2]) | or_reduce(a[len(a)//2:])

def registers(rr1, rr2, wr, wd, rw):
    bigone = "1" * 64
    bigzero = "0" * 64
    rr1_array = [Mux(eq_const(rr1, i), bigzero, bigone) for i in range(32)]
    rr2_array = [Mux(eq_const(rr2, i), bigzero, bigone) for i in range(32)]
    wr_array = [eq_const(wr, i) & rw for i in range(32)]
    regs = [Reg(Defer(64, lambda: Mux(wr_array[i], regs[i], wd))) for i in range(32)]
    rd1 = or_reduce([regs[i] | rr1_array[i] for i in range(32)])
    rd2 = or_reduce([regs[i] | rr2_array[i] for i in range(32)])
    return rd1, rd2
