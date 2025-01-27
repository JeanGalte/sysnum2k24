from lib_carotte import *
from registers import *
from utils import *
import ram
import alu

ARITH_PREFIX = 0b10011
LOAD_PREFIX = 0b0000011
STORE_PREFIX = 0b0100011
LUI = 0b0110111
AUIPC = 0b0010111
JAL = 0b1101111
JALR = 0b1100111

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

def decoder():
    pc = Reg(Defer(16, lambda: Mux(pc_change, pc_plus4, adder(pc, incr, Constant("0"))[0])))
    pc_plus4 = adder(pc, Constant ("0" * 13 + "100"), Constant("0"))[0]

    instr = ROM(14, 32, pc[2:])
    opcode = instr[0:7]

    rr1 = instr[15:20]
    rr2 = instr[20:25]
    wr = instr[7:12]
    funct3 = instr[12:15]
    funct7 = instr[25:]

    lui = eq_const(opcode, LUI, 7)
    big_imm = big_imm_gen(instr)
    small_imm = imm_gen(instr)

    jal  = eq_const(opcode, JAL, 7)
    jalr = eq_const(opcode, JALR, 7)
    auipc = eq_const(opcode, AUIPC, 7)
    write_pc_plus4 = jal | jalr
    pc_change = jal | jalr | auipc

    incr = Mux(auipc, Mux(jal, small_imm, jal_imm(instr)), big_imm)[:16]
    
    rw = eq_const(opcode, ARITH_PREFIX, 5) | lui | eq_const(opcode, LOAD_PREFIX, 7) | write_pc_plus4
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

    in2 = Mux(instr[5], small_imm, rd2)
    alu_out = alu.alu(rd1, in2, funct3, funct7)

    # ram
    ram_write2reg = eq_const(opcode, LOAD_PREFIX, 7)
    ram_write_en = eq_const(opcode, STORE_PREFIX, 7)

    ram_word_size = instr[12:14]
    ram_sign_extend = Not(instr[15])
    ram_read_addr, _ = adder(rd1, imm_gen(instr), Constant("0"))
    ram_write_addr, _ = adder(rd1, imm_gen_alt(instr), Constant("0"))
    ram_write_data = rd2

    ram_out = ram.ram_manager(10, ram_word_size, ram_sign_extend, ram_read_addr[:16], ram_write_en, ram_write_addr[:16], rd2)

    wd = multimux([lui, ram_write2reg, write_pc_plus4], [alu_out, big_imm, ram_out, Constant("0" * 64)])

def main():
    allow_ribbon_logic_operations(True)
    decoder()
