ARG PYTHON_VERSION=3.10-slim-buster

FROM python:${PYTHON_VERSION}

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir -p /code

WORKDIR /code

COPY requirements.txt /tmp/requirements.txt
RUN set -ex && \
    pip install --upgrade pip && \
    pip install -r /tmp/requirements.txt && \
    rm -rf /root/.cache/

RUN apt update 
RUN apt install -y --no-install-recommends apt-utils
RUN apt -y install curl 
RUN apt -y install libgomp1

COPY . /code

ENV DJANGO_SECRET_KEY "aN2lzZRtgGHAnQ40BeglAzbfKYLDaJluN3Gm994qPzsIYvD33L"
ENV DJANGO_DEBUG="False"

EXPOSE 8501

CMD ["./run.sh"]
