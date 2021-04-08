# docker build . --no-cache -t master_microservice
# docker container run --rm -it master_microservice bash

FROM ubuntu:20.04

ENV command "python manage.py test"

ADD ./ColoringMicroservice /ColoringMicroservice

RUN apt-get update
# RUN apt-get install software-properties-common -y && \
RUN apt-get install -y python-is-python3 python3-distutils curl && \
    curl https://bootstrap.pypa.io/get-pip.py | python
RUN pip install Django==3.2
# RUN apt-get install locales
# RUN locale-gen en_US.UTF-8
CMD ${command}