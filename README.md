# Un magnifique processeur !
## Assembleur
Le répertoire `asm` contient un assembleur pour notre processeur. Il a une fonctionnalité de simulateur, à condition de ne pas utiliser `jalr`, `lui`, `auipc` et des opérations en mémoire sur autre chose que 64 bits.

```
asm.exe [options] file.s
  -o   output file name
  -simulator   run the simulator, otherwise run the assembler
  -verbose   when used with --simulator, dump registers on every non-jump step
  -ram   when used with --simulator, sets the number of bytes in the simulated RAM (default 2048)
  -help  Display this list of options
  --help  Display this list of options
```
