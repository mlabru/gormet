#!/bin/bash

# language
# export LANGUAGE=pt_BR

echo ">>>>>>>>  ${USER}  <<<<<<<<<<<<<<<<"

# gorfog directory
GORFOG=~/Public/gorfog

# nome do computador
HOST=`hostname`

# get today's date
TDATE=`date '+%Y-%m-%d_%H-%M-%S'`

# home directory exists ?
if [ -d ${GORFOG} ]; then
    # set home dir
    cd ${GORFOG}
fi

# log file
LOGF="logs/gorfog.$HOST.$TDATE.log"

# logger
echo "Início de processamento: " $(date '+%Y-%m-%d %H:%M') > $LOGF

# ckeck if another instance of loader is running
DI_PID_GORFOG=`ps ax | grep -w python3 | grep -w gorfog.py | awk '{ print $1 }'`

if [ ! -z "$DI_PID_GORFOG" ]; then
    # log warning
    echo "[`date`]: process gorfog is already running. Waiting..." >> $LOGF
    # kill process
    kill -9 $DI_PID_GORFOG
    # wait 10s
    sleep 10
fi

# set PYTHONPATH
export PYTHONPATH="$PWD/."
# executa o loader
~/.poetry/bin/poetry run python3 gorfog.py $@ >> $LOGF 2>&1

# logger
echo "Fim de processamento: " $(date '+%Y-%m-%d %H:%M') >> $LOGF

# < the end >----------------------------------------------------------------------------------
