#!/bin/bash

cd ~/xrwise-website || exit

git lfs pull
git pull

docker build -t flask-app .

docker stop flask-app 2>/dev/null
docker rm flask-app 2>/dev/null

docker run -d \
  --network proxy \
  --env-file .env \
  --name flask-app \
  flask-app