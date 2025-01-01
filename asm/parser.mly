%{
  open Syntax
%}

%token <int> IMM
%token <int> REG
%token COMMA
%token <Syntax.op> OP
%token <Syntax.op> OPI
%token EOF
%start program
%type <instruction list> program

%%

instruction:
  | op = OP x1 = REG COMMA x2 = REG COMMA x3 = REG { Op (op, x1, x2, x3) }
  | op = OPI x1 = REG COMMA i = IMM COMMA x3 = REG
    { let i = if op = Sra then i lor (1 lsl 10) else i in Opi (op, x1, i, x3) }

program:
  | l = instruction* EOF { l }
