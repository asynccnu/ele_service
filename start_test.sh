#!/bin/sh

docker-compose -f docker-compose.test.yml stop
docker-compose -f docker-compose.test.yml build
docker-compose -f docker-compose.test.yml up -d && docker-compose -f docker-compose.test.yml logs ele_api_test
