#!/bin/bash

# cd ./moss

# run moss.jar file

java -cp moss.jar moss.Miner  ./moss/data/example1.smi -jS -s50 -v $*


# CLASSPATH="..:moss.jar"; export CLASSPATH

# java moss.Miner data/example1.smi -jS -s50 -v $*

#java moss.Miner data/example2.smi -jS -s-2 -v $*
#java moss.Miner data/noperfect.smi -jN -s100 -v $*
#java moss.Miner data/noperfect.smi -jN -s50 -r5:6 -R -v $*
#java moss.Miner data/chains.smi -jN -C -s75 -v $*
#java moss.Miner data/rings1.smi -jN -s-1 -r5:6 -R +q -v $*
#java moss.Miner data/rings2.smi -jN -s-1 -r5:6 -R +q -v $*
#java moss.Miner data/rings3.smi -jN -s-1 -r5:6 -R +q -v $*
#java moss.Miner data/atomprop.smi -s-1 -v +c +a $*

#java moss.Miner data/steroids.smi -s100 -r5:6 -R -e -p $*
#java moss.Miner data/steroids.smi -s100 -r5:6 -R -e +p $*
#java moss.Miner data/steroids.smi -s100 -r5:6 -R +e -p $*
#java moss.Miner data/steroids.smi -s100 -r5:6 -R +e +p $*

#java moss.Miner data/steroids.smi -s100 -e -p -q $*
#java moss.Miner data/steroids.smi -s100 -e +p -q $*
#java moss.Miner data/steroids.smi -s100 +e -p -q $*
#java moss.Miner data/steroids.smi -s100 -e -p +q $*
#java moss.Miner data/steroids.smi -s100 +e -p +q $*
#java moss.Miner data/steroids.smi -s100 +e +p +q $*

#java moss.Miner data/maxsrc.smi -jN -s100 -e -p +q $*
#java moss.Miner data/maxsrc.smi -jN -s100 -e -p +q -g $*
#java moss.Miner data/right.smi  -jO -s100 -e -p +q $*
#java moss.Miner data/right.smi  -jO -s100 -e -p +q -g $*

#java moss.Miner -inel -onel data/ttt_notwin.nel moss.sub
