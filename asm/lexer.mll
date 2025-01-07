{
  open Parser
  open Syntax
}

rule lexer = parse
  | [' ' '\t' '\n' '\r'] { lexer lexbuf }
  | ';' [^'\n']* '\n' { lexer lexbuf }
  | eof { EOF }
  | "or" { OP Or }
  | "and" { OP And }
  | "add" { OP Add }
  | "sub" { OP Sub }
  | "sll" { OP Sll }
  | "slt" { OP Slt }
  | "sltu" { OP Sltu }
  | "xor" { OP Xor }
  | "srl" { OP Srl }
  | "sra" { OP Sra }
  | "ori" { OPI Or }
  | "andi" { OPI And }
  | "addi" { OPI Add }
  | "slli" { OPI Sll }
  | "slti" { OPI Slt }
  | "sltiu" { OPI Sltu }
  | "xori" { OPI Xor }
  | "srli" { OPI Srl }
  | "srai" { OPI Sra }
  | "lb" { LOAD 0b000 }
  | "lh" { LOAD 0b001 }
  | "lw" { LOAD 0b010 }
  | "ld" { LOAD 0b011 }
  | "lbu" { LOAD 0b100 }
  | "lhu" { LOAD 0b101 } 
  | "lwu" { LOAD 0b110 }
  | "sb" { STORE 0b000 }
  | "sh" { STORE 0b001 }
  | "sw" { STORE 0b010 }
  | "sd" { STORE 0b011 }
  | ['0' - '9']* as s { IMM (int_of_string s) }
  | ',' { COMMA }
  | '(' { LPAR }
  | ')' { RPAR }
  | 'x' (['0'-'9']+ as s)
    { let n = int_of_string s in
      if n < 0 || n > 31 then (Printf.eprintf "Invalid register: %d" n; exit 0)
      else REG n }
  | _ as c { Printf.eprintf "Unknown character: %c" c; exit 1 }

{

}
