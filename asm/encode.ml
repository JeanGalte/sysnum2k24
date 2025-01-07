open Syntax

module Op : sig
  type t = op
  val compare : t -> t -> int
end = struct
  type t = op
  let compare = compare
end

module OMap = Map.Make(Op)

let funct3 =
  [Add, 0b000; Sub, 0b000; Sll, 0b001; Slt, 0b010; Sltu, 0b011; Xor, 0b100;
   Srl, 0b101; Sra, 0b101; Or, 0b110; And, 0b111]
  |> List.to_seq |> OMap.of_seq
let funct7 = [Sub, 0b0100000; Sra, 0b0100000] |> List.to_seq |> OMap.of_seq

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
