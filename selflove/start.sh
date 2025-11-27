#!/bin/bash
docker stop selflove || true
docker rm selflove || true
docker build -t selflove .
docker run -dit -p40111:40111 --name selflove selflove