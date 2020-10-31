FROM python:3.8

WORKDIR /usr/src/app

RUN pip install pipenv
COPY Pipfile .
COPY Pipfile.lock .
RUN pipenv install --deploy --system

RUN mkdir pax0r_ddns_server
COPY pax0r_ddns_server/ pax0r_ddns_server/
COPY config.yaml .

CMD python -m pax0r_ddns_server
