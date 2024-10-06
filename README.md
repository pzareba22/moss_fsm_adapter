# moss_fsm_adapter

What has to be done?
- cd into  moss_fsm_adapter/moss/moss
- run make all -> then you can run `./run` from terminal. 

you get the following output:
```
kacper@MacBook-Pro-kacper moss % ./run 

moss.Miner - molecular substructure miner (MoSS)
version 8.3 (2022.11.19)    (c) 2002-2022 Christian Borgelt
parsing seed description ... [1 atom(s), 0 bond(s)] done.
parsing excluded atom types ... [1 atom(s)] done.
reading molecules ... [6 (6+0) molecule(s)] done [0.0s].
marking bridges ... [6 molecule(s)] done [0.0s].
masking atom and bond types ... [6 molecule(s)] done [0.0s].
preparing/recoding molecules ... [6 molecule(s)] done [0.001s].
embedding the seed ... [6 (6+0) molecule(s)] done [0.001s].
searching for substructures ... 
S  a:1 b:1 c:1 d:1 e:1 f (6)
   S-C  a:1 b:2 c:2 d:1 e:1 f (6)
      S(-O)-C  a:2 b:2 c:2 f (4)
         S(-O)(-N)-C  a:2 b:2 c:2  (3)
      S(-N)-C  a:1 b:2 c:2 d:1 e (5)
         S(-N)-C-C  a:1 b:1 d (3)
      S(-C)=N  d:1 e:1 f (3)
      S-C-C  a:1 b:1 d (3)
[6 substructure(s)] done [0.006s].
search statistics:
maximum search tree height   : 3
number of search tree nodes  : 8
number of created fragments  : 21
number of created embeddings : 84
insufficient support pruning : 10
perfect extension pruning    : 1
equivalent sibling pruning   : 0
canonical form pruning       : 0
ring order pruning           : 0
duplicate fragment pruning   : 0
non-closed fragments         : 2
fragments with open rings    : 0
fragments with invalid chains: 0
auxiliary invalid fragments  : 0
accesses to repository       : 0
comparisons with fragments   : 0
actual isomorphism tests     : 0
comparisons with embeddings  : 0
```

## Questions
- We want to return the output in some format to be parsed by the user right?
- Is there any expected output format?
- What is the expected input format? is it compatible with .smi files?

 