#!/usr/bin/env bash

screen -d -m -S pipeline bash -c 'cd $HOME/tesis2 && source && source venv_caleuche/bin/activate && python pipeline.py'