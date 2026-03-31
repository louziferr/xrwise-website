#!/bin/bash

cd ~/xrwise-website || exit

git pull

docker build -t flask-app .

docker stop flask-app 2>/dev/null
docker rm flask-app 2>/dev/null

docker run -d -p 8081:5000 --name flask-app flask-app