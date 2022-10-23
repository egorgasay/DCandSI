FROM ubuntu:latest
COPY . /DCSI
WORKDIR /DCSI
RUN apt-get update
RUN apt-get install -y unixodbc-dev
RUN apt-get install -y python3 python3-pip
RUN pip install -r requirements_linux.txt