from lib_carotte import *
from registers import *

ARITH_PREFIX = 0b10011

# À modifier quand on aura fait l'ALU
def full_adder(a: Variable, b: Variable, c: Variable) -> typing.Tuple[Variable, Variable]:
    '''1-bit full adder implementation'''
    tmp = a ^ b
    return (tmp ^ c, (tmp & c) | (a & b))

def adder(a: Variable, b: Variable, c_in: Variable, i: int | None = None) -> typing.Tuple[Variable, Variable]:
    '''n-bit full-adder implementation'''
    assert a.bus_size == b.bus_size
    if i is None:
        i = a.bus_size-1
    assert 0 <= i < a.bus_size
    if i == 0:
        return full_adder(a[i], b[i], c_in)
    (res_rest, c_rest) = adder(a, b, c_in, i-1)
    (res_i, c_out) = full_adder(a[i], b[i], c_rest)
    return (res_rest + res_i, c_out)

def pc():
    pc = Reg(Defer(16, lambda: adder(pc, Constant("0" * 15 + "1"), Constant("0"))[0]))
    return pc

def alu_mini(in1, in2, funct7, funct3):
    res = in1 | in2
    zero = Not(eq_const(res, 0, 64))
    return res, zero

def imm_gen(instr):
    return instr[20:] + Constant("0" * 52)

def decoder():
    rpc = pc()
    instr = ROM(16, 32, rpc)
    rr1 = instr[15:20]
    rr2 = instr[20:25]
    wr = instr[7:12]
    opcode = instr[0:7]
    rw = eq_const(opcode, ARITH_PREFIX, 5)
    funct3 = instr[12:15]
    funct7 = instr[30]

    # registers
    bigone = Constant("1" * 64)
    bigzero = Constant("0" * 64)
    rr1_array = [bigzero] + [Mux(eq_const(rr1, i, 5), bigzero, bigone) for i in range(1, 32)]
    rr2_array = [bigzero] + [Mux(eq_const(rr2, i, 5), bigzero, bigone) for i in range(1, 32)]
    wr_array = [eq_const(wr, i, 5) & rw for i in range(32)]
    regs = [Reg(Defer(64, lambda i=i: Mux(wr_array[i], regs[i], wd))) for i in range(32)]
    rd1 = or_reduce([regs[i] & rr1_array[i] for i in range(32)])
    rd2 = or_reduce([regs[i] & rr2_array[i] for i in range(32)])

    for i, r in enumerate(regs):
        r.set_as_output("r" + str(i))

    in2 = Mux(instr[5], imm_gen(instr), rd2)
    wd, zero = alu_mini(rd1, in2, funct7, funct3)

def main():
    allow_ribbon_logic_operations(True)
    decoder()
