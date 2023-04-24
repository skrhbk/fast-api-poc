#!/bin/bash

docker run --name mongo4 -v $(pwd)/data:/data/db -d -p 27017:27017 --rm mongo:4.1

docker run --name my-mongo -v $(pwd)/conf:/etc/mongo -v $(pwd)/data:/data/db -d mongo --config /etc/mongo/mongod.conf

docker run -it --rm mongo mongosh --host 192.168.50.74 -u admin -p admin --authenticationDatabase admin admin

use products


db.runCommand({connectionStatus : 1})



####

docker network create -d bridge mongo-network  # 建立 Docker Network
docker network ls

docker run --name my-mongo --network mongo-network --rm -p 27017:27017 -p 28017:28017 -v D:/Workspace/mongo/data:/data/db -e MONGO_INITDB_ROOT_USERNAME=admin -e MONGO_INITDB_ROOT_PASSWORD=admin -d mongo

docker run --name my-mongo-express --network mongo-network -e ME_CONFIG_MONGODB_SERVER=my-mongo -e ME_CONFIG_MONGODB_ADMINUSERNAME=admin -e ME_CONFIG_MONGODB_ADMINPASSWORD=admin -e ME_CONFIG_BASICAUTH_USERNAME=express -e ME_CONFIG_BASICAUTH_PASSWORD=express -p 8081:8081 -d mongo-express:latest

docker run -it --rm --network mongo-network mongo mongosh --host my-mongo -u admin -p admin --authenticationDatabase admin admin