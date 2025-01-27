open Syntax

type env = {ram : Bytes.t; regs : Int64.t array; print_step : bool}

let rec sim env prog i =
  let nojmp = ref true and noprint = ref false in
  begin match prog.(i) with
  | Op (op, r2, r1, dest) ->
    let res = begin match op with
      | Or -> Int64.logor env.regs.(r1) env.regs.(r2)
      | And -> Int64.logand env.regs.(r1) env.regs.(r2)
      | Add -> Int64.add env.regs.(r1) env.regs.(r2)
      | Sub -> Int64.sub env.regs.(r1) env.regs.(r2)
      | Sll -> Int64.shift_left env.regs.(r1) (Int64.to_int env.regs.(r2))
      | Slt -> if Int64.compare env.regs.(r1) env.regs.(r2) < 0 then Int64.one else Int64.zero
      | Sltu -> if Int64.unsigned_compare env.regs.(r1) env.regs.(r2) < 0 then Int64.one else Int64.zero
      | Xor -> Int64.logxor env.regs.(r1) env.regs.(r2)
      | Srl -> Int64.shift_right_logical env.regs.(r1) (Int64.to_int env.regs.(r2))
      | Sra -> Int64.shift_right env.regs.(r1) (Int64.to_int env.regs.(r2))
    end in
    env.regs.(dest) <- res
  | Opi (op, r1, imm, dest) ->
    let res = begin match op with
      | Or -> Int64.logor env.regs.(r1) (Int64.of_int imm)
      | And -> Int64.logand env.regs.(r1) (Int64.of_int imm)
      | Add -> Int64.add env.regs.(r1) (Int64.of_int imm)
      | Sub -> Int64.sub env.regs.(r1) (Int64.of_int imm)
      | Sll -> Int64.shift_left env.regs.(r1) imm
      | Slt -> if Int64.compare env.regs.(r1) (Int64.of_int imm) < 0 then Int64.one else Int64.zero
      | Sltu -> if Int64.unsigned_compare env.regs.(r1) (Int64.of_int imm) < 0 then Int64.one else Int64.zero
      | Xor -> Int64.logxor env.regs.(r1) (Int64.of_int imm)
      | Srl -> Int64.shift_right_logical env.regs.(r1) imm
      | Sra -> Int64.shift_right env.regs.(r1) imm
    end in
    env.regs.(dest) <- res
  | Load (_, offset, r2, r1) ->
    let addr = (Int64.to_int env.regs.(r2)) + offset in
    env.regs.(r1) <- Bytes.get_int64_le env.ram addr
  | Store (_, r1, offset, r2) ->
    let addr = (Int64.to_int env.regs.(r2)) + offset in
    Bytes.set_int64_le env.ram addr env.regs.(r1);
    print_endline (string_of_int r1);
    print_endline (Int64.to_string env.regs.(r1));
    print_endline (Int64.to_string (Bytes.get_int64_le env.ram addr))
  | Branch (bop, r1, r2, (_, addenvs)) ->
    noprint := true;
    let v1 = env.regs.(r1) and v2 = env.regs.(r2) in
    if match bop with
      | Eq -> v1 = v2
      | Ne -> v1 <> v2
      | Lt -> v1 < v2
      | Ge -> v1 >= v2
      | Ltu -> Int64.unsigned_compare v1 v2 < 0
      | Geu -> Int64.unsigned_compare v1 v2 >= 0
    then begin
      nojmp := false;
      sim env prog (!addenvs / 4)
    end
  | Jal (r, (_, addr)) ->
    noprint := true;
    env.regs.(r) <- Int64.of_int (4*i);
    nojmp := false;
    sim env prog (!addr / 4)
  | Nop -> noprint := true
  | _ -> failwith "pas trop implémenté"
  end;
  if not !noprint && (env.print_step || i+1 = Array.length prog) then begin
    print_endline "\nregister | value";
    print_endline "---------|------";
    Array.iteri (fun i n ->
      let s = (Int64.to_string n) in
      Printf.printf "x%-7d | %s\n" i s
  ) env.regs
  end;
  if !nojmp && i+1 < Array.length prog then sim env prog (i+1)

