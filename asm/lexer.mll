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
  | ['0' - '9']* as s { IMM (int_of_string s) }
  | ',' { COMMA }
  | 'x' (['0'-'9']+ as s)
    { let n = int_of_string s in
      if n < 0 || n > 31 then (Printf.eprintf "Invalid register: %d" n; exit 0)
      else REG n }
  | _ as c { Printf.eprintf "Unknown character: %c" c; exit 1 }

{

}
