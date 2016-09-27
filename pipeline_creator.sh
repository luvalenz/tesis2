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

#standarized not_weighted
#ns=("100" "500" "1000" "5000")
#std="std_notweighted"
#
#for n in "${ns[@]}"
#do
#    screen_name=$std$n
#    echo $screen_name
#    screen -S $screen_name -dm bash -c "cd $HOME/tesis2; source venv_caleuche/bin/activate; python pipeline.py ${n} 250 10 20 std not"
#done

#different levels
#ns=("100" "500" "1000" "5000")
#levels=("10" "30" "40" "null")
#
#for n in "${ns[@]}"
#do
#    for level in "${levels[@]}"
#    do
#        screen_name="std${n}_level${level}"
#        echo $screen_name
#        screen -S $screen_name -dm bash -c "cd $HOME/tesis2; source venv_caleuche/bin/activate; python pipeline.py ${n} 250 10 ${level} std not"
#    done
#done


#different window size
ns=("100" "500" "1000" "5000")
sizes=("10" "20" "50" "100" "150" "200")

for n in "${ns[@]}"
do
    for size in "${sizes[@]}"
    do
        screen_name="std${n}_ws${size}"
        echo $screen_name
        screen -S $screen_name -dm bash -c "cd $HOME/tesis2; source venv_caleuche/bin/activate; python pipeline.py ${n} ${size} 10 20 std not"
    done
done