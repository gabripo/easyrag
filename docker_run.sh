#! /bin/bash

if [ $# -eq 0 ]
then
    echo  "Default host port used: 3000"
    HOST_PORT="3000"
else
    echo  "Specified host port will be used: $1"
    HOST_PORT=$1
fi

echo "Link to the project homepage: http://0.0.0.0:$HOST_PORT"
docker run -p $HOST_PORT:3000 -p 8501:8501 docker-easyrag