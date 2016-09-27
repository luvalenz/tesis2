#!/usr/bin/env bash
#standarized, semi, and not
#standardization=("std" "semi" "not")
#ns=("100" "500" "1000" "5000")
#
#for std in "${standardization[@]}"
#do
#    for n in "${ns[@]}"
#    do
#        screen_name=$std$n
#        echo $screen_name
#        screen -S $screen_name -dm bash -c "cd $HOME/tesis2; source venv_caleuche/bin/activate; python pipeline.py ${n} 250 10 20 ${std} weighted"
#    done
#done

#standarizednot_weighted
ns=("100" "500" "1000" "5000")
std="std_notweighted"

for n in "${ns[@]}"
do
    screen_name=$std$n
    echo $screen_name
    screen -S $screen_name -dm bash -c "cd $HOME/tesis2; source venv_caleuche/bin/activate; python pipeline.py ${n} 250 10 20 std not"
done