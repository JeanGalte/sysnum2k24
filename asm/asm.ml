let usage = "asm.exe [options] file.s"
let simulator = ref false
let print_step = ref false
let spec = [
  "--simulator", Arg.Set simulator, "  run the simulator, otherwise run the assembler";
  "--verbose", Arg.Set print_step, "  when used with --simulator, dump registers on every non-jump step";
]

let (%) f g = fun x -> f (g x)

let _ =
  let p = ref [] in
  let read_file f =
    let ic = open_in f in
    let lexbuf = Lexing.from_channel ic in
    p := Parser.program Lexer.lexer lexbuf;
    close_in ic in
  Arg.parse spec read_file "";
  if !simulator then
    Simulator.sim {Simulator.regs = Array.make 32 Int64.zero; Simulator.ram = Bytes.make 2048 '\000'; Simulator.print_step = !print_step} (Array.of_list !p) 0
  else begin
    let oc = open_out "out" in
    List.iter (output_string oc) (List.map (Emit.int32 % Encode.instruction) !p);
    close_out oc
  end
