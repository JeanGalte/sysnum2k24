%{
  open Syntax

  let pc = ref 0

  let labels = Hashtbl.create 17

  let get_label_ref s =
    match Hashtbl.find_opt labels s with
    | None ->
       let r = ref 0 in
       Hashtbl.add labels s r;
       r
    | Some r -> r
%}

%token <int> IMM
%token <int> REG
%token <Syntax.op> OP
%token <Syntax.op> OPI
%token <Syntax.bop> BOP
%token <int> STORE
%token <int> LOAD
%token <string> LABEL
%token LUI AUIPC JAL JALR
%token COMMA LPAR RPAR DCOL
%token EOF
%start program
%type <instruction list> program

%%

instruction:
  | op = OP x1 = REG COMMA x2 = REG COMMA x3 = REG
    { pc := !pc + 4; Op (op, x3, x2, x1) }
  | op = OPI x1 = REG COMMA x3 = REG COMMA i = IMM
    { let i = if op = Sra then i lor (1 lsl 10) else i in
      pc := !pc + 4;  Opi (op, x3, i, x1) }
  | size = LOAD x2 = REG COMMA i = IMM LPAR x1 = REG RPAR
    { pc := !pc + 4; Load (size, i, x1, x2) }
  | size = STORE i = IMM LPAR x2 = REG RPAR COMMA x1 = REG
    { pc := !pc + 4; Store (size, x1, i, x2) }
  | s = LABEL DCOL { get_label_ref s := !pc; Nop }
  | op = BOP x1 = REG COMMA x2 = REG COMMA s = LABEL
    { pc := !pc + 4; Branch (op, x1, x2, (!pc - 4, get_label_ref s)) }
  | JAL x = REG COMMA s = LABEL
    { pc := !pc + 4; Jal (x, (!pc - 4, get_label_ref s))}
  | JALR x1 = REG COMMA x2 = REG COMMA s = LABEL
    { pc := !pc + 4; Jalr (x1, x2, (!pc - 4, get_label_ref s))}
  | LUI x = REG COMMA i = IMM
    { pc := !pc + 4; Lui (x, i) }
  | AUIPC x = REG COMMA i = IMM
    { pc := !pc + 4; Auipc (x, i) }

program:
  | l = instruction* EOF { l }
