type reg = int
type imm = int
type size = int

type op = Or | And | Add | Sub | Sll | Slt | Sltu | Xor | Srl | Sra
type bop = Eq | Ne | Lt | Ge | Ltu | Geu

type address = int * int ref

type instruction
  = Op  of op * reg * reg * reg
  | Opi of op * reg * imm * reg
  | Load of size * imm * reg * reg
  | Store of size * reg * imm * reg
  | Branch of bop * reg * reg * address
  | Lui of reg * imm
  | Auipc of reg * imm
  | Jal of reg * address
  | Jalr of reg * reg * address
  | Nop
