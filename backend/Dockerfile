FROM python:3.8.13

WORKDIR /backend

COPY requirements.txt /backend

RUN pip3 install -r requirements.txt

COPY . .

RUN python3 -m grpc_tools.protoc -I proto --python_out=. --grpc_python_out=. proto/proto_site.proto

EXPOSE 50051

CMD ["python3", "-u", "app.py"]

