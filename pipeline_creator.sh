#!/usr/bin/env bash

#standarized, semi, and not

#declare -a standarization=('std' 'semi' 'not')
#a = 'hola'


screen -S hola -dm bash -c 'cd $HOME/tesis2; source venv_caleuche/bin/activate; python pipeline.py 2 250 10 20'