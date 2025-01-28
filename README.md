# Un magnifique processeur !
## Instruction de compilation
On peut récupérer le code avec : `git clone --recurse-submodules -j8 https://github.com/JeanGalte/sysnum2k24.git` et le compiler avec `./build.sh`. Cela crée un exécutable `cpu` qui lance le programme contenu dans `rom/prog` qui peut être assemblé avec `erasm`. Par défaut, il contient une horloge.
## Assembleur
Le répertoire `asm` contient un assembleur pour notre processeur. Il a une fonctionnalité de simulateur, à condition de ne pas utiliser `lui`, `auipc`, les branchements et sauts et des opérations en mémoire sur autre chose que 64 bits.

```
./erasm [options] file.s
  -o   output file name
  -simulator   run the simulator, otherwise run the assembler
  -verbose   when used with --simulator, dump registers on every non-jump step
  -ram   when used with --simulator, sets the number of bytes in the simulated RAM (default 2048)
  -help  Display this list of options
  --help  Display this list of options
```
