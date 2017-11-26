FROM python:3.6-slim

COPY requirements.txt /opt/app/
WORKDIR /opt/app
RUN pip install -r requirements.txt

COPY rest.py /opt/app
COPY config.py /opt/app

EXPOSE 8000

ENTRYPOINT ["/usr/local/bin/gunicorn", "rest:app"]

