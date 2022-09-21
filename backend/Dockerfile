FROM python:3.8.10

WORKDIR /backend

COPY requirements.txt /backend

RUN python3 -m pip install --upgrade pip

RUN pip3 install -r requirements.txt

COPY . .

RUN python3 -m grpc_tools.protoc -I proto --python_out=. --grpc_python_out=. proto/proto_site.proto

EXPOSE 50051


CMD ["tail", "-f", "/dev/null"]

