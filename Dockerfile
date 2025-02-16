FROM python:3.11
RUN apt update &&  apt install -y graphviz libgraphviz-dev
RUN mkdir -p /app/simprov
ADD pyproject.toml /app
COPY simprov/ /app/simprov
WORKDIR /app

RUN pip install .
EXPOSE 5000