open Syntax

module Op : sig
  type t = op
  val compare : t -> t -> int
end = struct
  type t = op
  let compare = compare
end

module OMap = Map.Make(Op)

module Bop : sig
  type t = bop
  val compare : t -> t -> int
end = struct
  type t = bop
  let compare = compare
end

module BOMap = Map.Make(Bop)

let funct3 =
  [Add, 0b000; Sub, 0b000; Sll, 0b001; Slt, 0b010; Sltu, 0b011; Xor, 0b100;
   Srl, 0b101; Sra, 0b101; Or, 0b110; And, 0b111]
  |> List.to_seq |> OMap.of_seq
let funct7 = [Sub, 0b0100000; Sra, 0b0100000] |> List.to_seq |> OMap.of_seq

let bop_map =
  [Eq, 0b000; Ne, 0b001; Lt, 0b100; Ge, 0b101; Ltu, 0b110; Geu, 0b111]
  |> List.to_seq |> BOMap.of_seq

let eval_address (n, r) =
  print_int (!r - n);
  !r - n

let instruction = function
  | Op (op, x1, x2, x3) ->
    0b0110011 lor (x3 lsl 7) lor (OMap.find op funct3 lsl 12) lor
    (x1 lsl 15) lor (x2 lsl 20) lor
    ((OMap.find_opt op funct7 |> Option.value ~default:0) lsl 25)
  | Opi (op, x1, i, x3) ->
    0b0010011 lor (x3 lsl 7) lor (OMap.find op funct3 lsl 12) lor
    (x1 lsl 15) lor (i lsl 20)
  | Load (size, i, x1, x3) ->
    0b0000011 lor (x3 lsl 7) lor (size lsl 12) lor (x1 lsl 15) lor (i lsl 20)
  | Store (size, x2, i, x1) ->
    0b0100011 lor ((i land 0b111) lsl 7) lor (size lsl 12) lor (x1 lsl 15) lor
    (x2 lsl 20) lor ((i lsr 4) lsl 25)
  | Nop -> -1
  | Lui (x, i) ->
    0b0110111 lor (x lsl 7) lor (i lsl 12)
  | Auipc (x, i) ->
    0b0010111 lor (x lsl 7) lor (i lsl 12)
  | Jal (x, a) ->
    let a = eval_address a in
    0b1101111 lor (x lsl 7) lor ((0b11111111 lsl 12) land a) lor
    ((0b1 land (a lsr 11)) lsl 20) lor ((0b11111111110 land a) lsl 20) lor
    ((0b1 land (a lsr 20)) lsl 31)
  | Jalr (x1, x2, a) ->
    let a = eval_address a in
    0b1100111 lor (x1 lsl 7) lor (x2 lsl 15) lor (a lsl 20)
  | Branch (bop, x1, x2, a) ->
    let a = eval_address a in
    0b1100011 lor
    (x1 lsl 15) lor (x2 lsl 20) lor (BOMap.find bop bop_map lsl 12) lor
    ((0b1 land (a lsr 11)) lsl 7) lor
    ((0b1111 land (a lsr 1)) lsl 8) lor
    ((0b111111 land (a lsr 5)) lsl 25) lor
    ((0b1 land (a lsr 12)) lsl 31)
  | Gtck x ->
    0b0001011 lor (x lsl 7)
  | Sdt (d, x) ->
    0b0101011 lor (x lsl 15) lor (d lsl 12)
  | Gdt (d, x) ->
    0b1011011 lor (x lsl 7) lor (d lsl 12)
