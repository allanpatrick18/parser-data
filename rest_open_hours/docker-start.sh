#!/bin/sh
docker stop Oracle PL/SQL
echo "parou container"
docker rm restaraunt
echo "removeu container"
docker build -t restaraunt .
docker run -d --name=restaraunt -p 9997:8080  restaraunt