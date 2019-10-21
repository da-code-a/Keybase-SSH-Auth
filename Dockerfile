FROM ubuntu
ENV KEYBASE_ALLOW_ROOT=1
RUN apt update
RUN apt install -y curl python3 python3-dev python3-pip
RUN curl --remote-name https://prerelease.keybase.io/keybase_amd64.deb
RUN apt install -y ./keybase_amd64.deb
COPY main.py /main.py
COPY models.py /models.py
COPY requirements.txt /requirements.txt
COPY docker_run.sh /docker_run.sh
RUN chmod +X /docker_run.sh
RUN pip3 install -r requirements.txt