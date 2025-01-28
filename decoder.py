from lib_carotte import *
from registers import *
from utils import *
import ram
import alu

ARITH_PREFIX = 0b100
LOAD_PREFIX = 0b00000
STORE_PREFIX = 0b01000
LUI = 0b01101
AUIPC = 0b00101
JAL = 0b11011
JALR = 0b11001
BOP = 0b11000

GET_TICK = 0b00010
SET_DATE = 0b01010
GET_DATE = 0b10110

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

def eq(d1, d2):
    n = d1.bus_size
    if n == 1:
        return ~ (d1 ^ d2)
    return eq(d1[:n//2], d2[:n//2]) & eq(d1[n//2:], d2[n//2:])

def imm_gen(instr):
    extension = instr[31]
    for _ in range(6):
        extension = extension + extension
    return instr[20:] + extension[:52]

def imm_gen_alt(instr):
    extension = instr[31]
    for _ in range(6):
        extension = extension + extension
    return instr[7:12] + instr[25:] + extension[:52]

def big_imm_gen(instr):
    extension = instr[31]
    for _ in range(5):
        extension = extension + extension
    return Constant("0" * 12) + instr[12:] + extension

def jal_imm(instr):
    extension = instr[31]
    for _ in range(6):
        extension = extension + extension
    return Constant("0") + instr[21:30] + instr[20] + instr[12:20] + extension[:45]

def bop_imm(instr):
    extension = instr[31]
    for _ in range(6):
        extension = extension + extension
    return Constant("0") + instr[8:12] + instr[25:31] + instr[7] + extension[:52]

def decoder():
    pc = Reg(Defer(16, lambda: Mux(pc_change, pc_plus4, adder(pc, incr, Constant("0"))[0])))
    pc_plus4 = adder(pc, Constant ("0" * 13 + "100"), Constant("0"))[0]


    instr = ROM(14, 32, pc[2:])
    instr.rename("prog")
    opcode = instr[2:7]

    rr1 = instr[15:20]
    rr2 = instr[20:25]
    wr = instr[7:12]
    bop = eq_const(opcode, BOP, 5)

    jal  = eq_const(opcode, JAL, 5)
    jalr = eq_const(opcode, JALR, 5)
    auipc = eq_const(opcode, AUIPC, 5)
    write_pc_plus4 = jal | jalr
    pc_change = jal | jalr | auipc | bop
    
    funct3 = Mux(bop, instr[12:15], instr[13:15] + Constant("0"))
    funct7 = Mux(bop, instr[25:], Constant("0" * 7))
    arith_op = eq_const(opcode, ARITH_PREFIX, 3)

    lui = eq_const(opcode, LUI, 5)
    big_imm = big_imm_gen(instr)
    small_imm = imm_gen(instr)

    load = eq_const(opcode, LOAD_PREFIX, 5)

    get_tick = eq_const(opcode, GET_TICK, 5)
    set_date = eq_const(opcode, SET_DATE, 5)
    get_date = eq_const(opcode, GET_DATE, 5)
    
    rw = arith_op | lui | load | write_pc_plus4 | get_tick | get_date
    # registers
    bigone = Constant("1" * 64)
    bigzero = Constant("0" * 64)
    rr1_array = [bigzero] + [Mux(eq_const(rr1, i, 5), bigzero, bigone) for i in range(1, 32)]
    rr2_array = [bigzero] + [Mux(eq_const(rr2, i, 5), bigzero, bigone) for i in range(1, 32)]
    wr_array = [eq_const(wr, i, 5) & rw for i in range(32)]
    regs = [bigzero] + [Reg(Defer(64, lambda i=i: Mux(wr_array[i], regs[i], wd))) for i in range(1, 32)]
    rd1 = or_reduce([regs[i] & rr1_array[i] for i in range(32)])
    rd2 = or_reduce([regs[i] & rr2_array[i] for i in range(32)])

    for i, r in enumerate(regs):
        r.set_as_output("r" + str(i))

    in2 = Mux(instr[5], small_imm, rd2)
    alu_out = alu.alu(rd1, in2, funct3, funct7)

    # ram
    ram_write2reg = load
    ram_write_en = eq_const(opcode, STORE_PREFIX, 5)

    ram_word_size = instr[12:14]
    ram_sign_extend = Not(instr[15])
    ram_read_addr, _ = adder(rd1, imm_gen(instr), Constant("0"))
    ram_write_addr, _ = adder(rd1, imm_gen_alt(instr), Constant("0"))
    ram_write_data = rd2

    ram_out = ram.ram_manager(10, ram_word_size, ram_sign_extend,
                              ram_read_addr[:16], ram_write_en,
                              ram_write_addr[:16], rd2)

    # jump
    reg_eq = eq(rd1, rd2)
    cmp_res = Mux(eq_const(instr[13:15], 0b00, 2), alu_out[0], reg_eq) ^ instr[12]
    
    incr = Mux(auipc,
               Mux(jal,
                   Mux(bop,
                       adder(small_imm, rd1, Constant("0"))[0],
                       Mux(cmp_res, Constant("0" * 61 + "100"), bop_imm(instr))),
                   jal_imm(instr)),
               big_imm)[:16]

    # clock
    tick = ROM(1, 64, Constant("0"))
    tick.set_as_output("tick")

    
    date = RAM(3, 64, funct3, set_date, funct3, rd1)
    date.rename("date")

    wd = Mux(arith_op,
             Mux(lui,
                 Mux(ram_write2reg,
                     Mux(write_pc_plus4,
                         Mux(get_date, tick, date),
                         pc_plus4 + Constant("0" * 48)),
                     ram_out), big_imm), alu_out)

def main():
    allow_ribbon_logic_operations(True)
    decoder()
