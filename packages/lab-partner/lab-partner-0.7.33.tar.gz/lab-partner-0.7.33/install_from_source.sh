#!/bin/bash

set -e

. ./build.sh

echo "Copying lab-partner wheel from docker image"
container_id=$(docker create enclarify/lab-partner-packages:$(version))
docker cp ${container_id}:/opt/lab/dist/init/lab_partner-$(version)-py3-none-any.whl - > /tmp/lab_partner-$(version)-py3-none-any.whl
docker rm -f ${container_id}

echo "Pushing Docker images to Docker Hub"
docker push enclarify/lab-partner-cli:$(version)
#docker push enclarify/lab-partner-jupyter:$(version)

echo "Installing lab-partner on host"
pip3 install --upgrade --force-reinstall /tmp/lab_partner-$(version)-py3-none-any.whl


#-rw-r--r--  1 runner   docker    9728 May 28 17:35 lab_partner-0.7.19-py3-none-any.whl
#-rw-r--r--  1 runner   docker   14848 May 28 17:35 lab_partner_utils-0.7.19-py3-none-any.whl