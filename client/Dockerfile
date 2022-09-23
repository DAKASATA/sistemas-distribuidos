FROM python:3.8.13

WORKDIR /client

COPY proto_site.proto ./

COPY requirements.txt /client

RUN pip3 install -r requirements.txt

RUN python3 -m grpc_tools.protoc -I./ --python_out=. --grpc_python_out=. ./proto_site.proto

ENV FLASK_APP=main.py
ENV FLASK_RUN_HOST=0.0.0.0

EXPOSE 8000
COPY . .
CMD ["flask", "run"]