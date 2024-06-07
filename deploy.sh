#!/bin/bash

docker build -t 'docker-test' -f 'Dockerfile.local' .

docker run -p 5001:5001 'docker-test'