FROM keybaseio/client
ENV KEYBASE_SERVICE=1
COPY main.py /main.py
COPY models.py /models.py
COPY requirements.txt /requirements.txt
RUN pip install -r requirements.txt
RUN python3 main.py
EXPOSE 5000