#!/usr/bin/env bash

#standarized, semi, and not

#declare -a standarization=('std' 'semi' 'not')
A = 'chao'


screen -S $A -dm bash -c 'cd $HOME/tesis2; source venv_caleuche/bin/activate; python pipeline.py 2 250 10 20'