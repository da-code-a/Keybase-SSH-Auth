FROM ubuntu
EXPOSE 5000
RUN apt update
RUN curl --remote-name https://prerelease.keybase.io/keybase_amd64.deb
RUN apt install -y ./keybase_amd64.deb
RUN keybase oneshot -u $KEYBASE_USERNAME --paperkey $KEYBASE_PAPERKEY
RUN apt install python3 virtualenv python3-dev build-essential python3-pip
RUN mkdir /mfa_server
COPY main.py /mfa_server/main.py
COPY models.py /mfa_server/models.py
COPY requirements.txt /mfa_server/requirements.txt
RUN cd /mfa_server
RUN virtualenv -p `which python3` env
RUN source env/bin/activate
RUN pip install -r requirements.txt
RUN python3 main.py