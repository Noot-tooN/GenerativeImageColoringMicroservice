# docker build . --no-cache -t master_microservice
# docker container run --rm -it master_microservice bash

FROM ubuntu:20.04

ENV listening_port 8000
ENV command "python manage.py runserver 0.0.0.0:${listening_port}"

ADD ./ColoringMicroservice /ColoringMicroservice
EXPOSE ${listening_port}

RUN apt-get update
# RUN apt-get install software-properties-common -y && \
RUN apt-get install -y python-is-python3 python3-distutils python3-dev gcc curl && \
    curl https://bootstrap.pypa.io/get-pip.py | python
RUN pip install Django==3.2 torch==1.7.1 torchvision fastai==2.3.0

WORKDIR /ColoringMicroservice
RUN python manage.py makemigrations && python manage.py migrate
# RUN apt-get install locales
# RUN locale-gen en_US.UTF-8
CMD ${command}