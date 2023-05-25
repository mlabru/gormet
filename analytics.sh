#!/bin/bash

# language
# export LANGUAGE=pt_BR

echo ">>>>>>>>  ${USER}  <<<<<<<<<<<<<<<<"

# gormet directory
GORMET=~/Public/gormet

# nome do computador
HOST=`hostname`

# get today's date
TDATE=`date '+%Y-%m-%d_%H-%M-%S'`

# home directory exists ?
if [ -d ${GORMET} ]; then
    # set home dir
    cd ${GORMET}
fi

# log file
LOGF="logs/analytics.$HOST.$TDATE.log"

# logger
echo "Início de processamento: " $(date '+%Y-%m-%d %H:%M') > $LOGF

# ckeck if another instance of loader is running
DI_PID_GORMET=`ps ax | grep -w python3 | grep -w analytics.py | awk '{ print $1 }'`

if [ ! -z "$DI_PID_GORMET" ]; then
    # log warning
    echo "[`date`]: process analytics is already running. Waiting..." >> $LOGF
    # kill process
    kill -9 $DI_PID_GORMET
    # wait 10s
    sleep 10
fi

# set PYTHONPATH
export PYTHONPATH="$PWD/."
# executa o loader
~/.poetry/bin/poetry run python3 analytics.py $@ >> $LOGF 2>&1

# logger
echo "Fim de processamento: " $(date '+%Y-%m-%d %H:%M') >> $LOGF

# < the end >----------------------------------------------------------------------------------
