let int32 n =
  if n >= 0 then
    String.init 32 (fun i -> if (n lsr (31 - i)) land 1 = 1 then '1' else '0')
  else ""
