#!/usr/bin/env bash

#standarized, semi, and not

declare -a standarization=('std' 'semi' 'not')
declare -a ns=('100', '500', '1000', '5000')

for std in "${standarization[@]}"
do
    for n in "${ns[@]}"
    do
        screen_name = $std$ns
        screen -S $screen_name -dm bash -c 'cd $HOME/tesis2; source venv_caleuche/bin/activate; python pipeline.py {$n} 250 10 20 {$std} weighted'
    done
done
