FROM python:3

WORKDIR /usr/src/app

RUN pip install dependency-injector
RUN pip install dnslib
RUN pip install sanic
RUN pip install dependency-injector[yaml]

RUN mkdir pax0r_ddns_server
COPY pax0r_ddns_server/ pax0r_ddns_server/
COPY config.yaml .

CMD python -m pax0r_ddns_server
