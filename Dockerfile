FROM amd64/python:3.6

ADD . .
WORKDIR /

RUN pip3 install -r requirements.txt

CMD /bin/bash