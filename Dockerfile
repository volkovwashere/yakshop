FROM python:3.8-alpine

WORKDIR /yakshop/

COPY src /yakshop/src/
COPY logs /yakshop/logs/
COPY properties /yakshop/properties/
COPY requirements.txt /yakshop/requirements.txt
RUN pip install -r /yakshop/requirements.txt
ENV PYTHONPATH "${PYTHONPATH}:/yakshop/src"


CMD uvicorn --host=0.0.0.0 --port=8000 yakshop.app:app
