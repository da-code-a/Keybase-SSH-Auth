FROM ubuntu
ENV KEYBASE_ALLOW_ROOT=1
ENV KB_TYPE=changeme
ENV KB_TEAM=changeme
ENV KB_USER=changeme
ENV KB_CHANNEL=changeme
ENV AUTH_TOKEN=changeme
ENV FLASK_ENV=changeme
ENV KEYBASE_USERNAME=changeme
ENV KEYBASE_PAPERKEY=changeme
RUN apt update
RUN apt install -y curl python3 python3-dev python3-pip
RUN curl --remote-name https://prerelease.keybase.io/keybase_amd64.deb
RUN apt install -y ./keybase_amd64.deb
COPY main.py /main.py
COPY models.py /models.py
COPY functions.py /functions.py
COPY requirements.txt /requirements.txt
COPY docker_run.sh /docker_run.sh
RUN chmod +x /docker_run.sh
RUN pip3 install -r requirements.txt
EXPOSE 5000
CMD ["/docker_run.sh"]