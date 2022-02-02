FROM python:3.8-slim

WORKDIR /invoice-reader/

COPY src /invoice-reader/src/
COPY logs /invoice-reader/logs/
COPY properties /invoice-reader/properties/
COPY ml-assets /invoice-reader/ml-assets/
COPY requirements.txt /invoice-reader/requirements.txt
RUN pip install -r /invoice-reader/requirements.txt
ENV PYTHONPATH "${PYTHONPATH}:/invoice-reader/src"


CMD python invoice_reader/main.py
