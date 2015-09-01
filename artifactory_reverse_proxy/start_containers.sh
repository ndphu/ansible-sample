#!/bin/sh
docker start artifactory_server
docker start artifactory_reverse_proxy
sleep 2
./proxy-up.yml

