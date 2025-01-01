type reg = int
type imm = int

type op = Or | And | Add | Sub | Sll | Slt | Sltu | Xor | Srl | Sra

type instruction
  = Op  of op * reg * reg * reg
  | Opi of op * reg * imm * reg
