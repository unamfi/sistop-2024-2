#!/bin/bash
current_commit=$(git rev-parse HEAD | cut -c 1-8)
autoIncrement=$(docker image list | grep sisop_$current_commit | wc -l)
((autoIncrement++))
if [[ $(pwd) != *"sistop-2024-2/proyectos/AguilarErick" ]]; then
    echo "No estas en la carpeta correcta"
    exit 1
fi
tag="sisop_$current_commit:v$autoIncrement"
docker build -t $tag -f Dockerfile.prod .
clear
docker run --rm $tag