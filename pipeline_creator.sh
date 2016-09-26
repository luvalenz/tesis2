#!/usr/bin/env bash

#standarized, semi, and not

#declare -a standarization=('std' 'semi' 'not')
#a = 'hola'


screen -dm -S hola bash -c 'cd $HOME/tesis2; source venv_caleuche/bin/activate; python pipeline.py'