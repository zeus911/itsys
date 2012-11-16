#!/bin/sh

PATH=/home/david/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
port=9002
#ps ax | grep $port | grep -v "grep" | awk '{print $2}' | xargs kill
homedir=/home/david/Publish/itsys
python $homedir/start.py 127.0.0.1:$port >/dev/null 2>&1 &

exit 0
