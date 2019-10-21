FROM ubuntu
EXPOSE 5000
RUN apt update
RUN apt install -y python3 virtualenv python3-dev build-essential python3-pip curl git
RUN curl --remote-name https://prerelease.keybase.io/keybase_amd64.deb
RUN apt install -y ./keybase_amd64.deb
RUN useradd -ms /bin/bash keybaseuser
USER keybaseuser
WORKDIR /home/keybaseuser
RUN git clone https://github.com/DonaldKBrown/Keybase-SSH-Auth
RUN keybase oneshot -u $KEYBASE_USERNAME --paperkey $KEYBASE_PAPERKEY
RUN cd Keybase-SSH-AUTH
RUN virtualenv -p `which python3` env
RUN source env/bin/activate
RUN pip install -r requirements.txt
RUN python3 main.py &