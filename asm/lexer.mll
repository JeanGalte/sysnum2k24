{
  open Parser
  open Syntax
}

let ident = (['a'-'z'] | ['A'-'Z']) (['a'-'z'] | ['A'-'Z'] | '_' | ['0'-'9'])*

rule lexer = parse
  | [' ' '\t' '\n' '\r'] { lexer lexbuf }
  | '#' [^'\n']* '\n' { lexer lexbuf }
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
  | "orw" { OP Or }
  | "andw" { OP And }
  | "addw" { OP Add }
  | "subw" { OP Sub }
  | "sllw" { OP Sll }
  | "sltw" { OP Slt }
  | "sltuw" { OP Sltu }
  | "xorw" { OP Xor }
  | "srlw" { OP Srl }
  | "sraw" { OP Sra }
  | "oriw" { OPI Or }
  | "andiw" { OPI And }
  | "addiw" { OPI Add }
  | "slliw" { OPI Sll }
  | "sltiw" { OPI Slt }
  | "sltiuw" { OPI Sltu }
  | "xoriw" { OPI Xor }
  | "srliw" { OPI Srl }
  | "sraiw" { OPI Sra }
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
  | "beq" { BOP Eq }
  | "bne" { BOP Ne }
  | "blt" { BOP Lt }
  | "bge" { BOP Ge }
  | "bltu" { BOP Ltu }
  | "bgeu" { BOP Geu }
  | "jal" { JAL }
  | "jalr" { JALR }
  | "lui" { LUI }
  | "auipc" { AUIPC }
  | "gyear" { GDT 0b000 }
  | "gmon" { GDT 0b001 }
  | "gday" { GDT 0b010 }
  | "ghour" { GDT 0b011 }
  | "gmin" { GDT 0b100 }
  | "gsec" { GDT 0b101 }
  | "syear" { SDT 0b000 }
  | "smon" { SDT 0b001 }
  | "sday" { SDT 0b010 }
  | "shour" { SDT 0b011 }
  | "smin" { SDT 0b100 }
  | "ssec" { SDT 0b101 }
  | "gtck" { GTCK }
  | '-'? ['0' - '9']* as s { IMM (int_of_string s) }
  | ',' { COMMA }
  | '(' { LPAR }
  | ')' { RPAR }
  | ':' { DCOL }
  | 'x' (['0'-'9']+ as s)
    { let n = int_of_string s in
      if n < 0 || n > 31 then (Printf.eprintf "Invalid register: %d" n; exit 0)
      else REG n }
  | ident as s { LABEL s }
  | _ as c { Printf.eprintf "Unknown character: %c" c; exit 1 }

{

}
