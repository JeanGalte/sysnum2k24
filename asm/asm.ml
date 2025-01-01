let _ =
  let read_file f =
    let ic = open_in f in
    let lexbuf = Lexing.from_channel ic in
    let p = Parser.program Lexer.lexer lexbuf in
    close_in ic;
    let oc = open_out "out" in
    List.iter (output_string oc) (List.map (Fun.compose Emit.int32 Encode.instruction ) p);
    close_out oc
  in Arg.parse [] read_file ""
