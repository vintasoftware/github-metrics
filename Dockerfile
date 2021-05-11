FROM python:3.9
ENV PYTHONUNBUFFERED 1
ARG UID=1000
ARG build_env
ENV BUILD_ENV ${build_env}

RUN apt-get update
RUN apt-get install -qq -y curl
RUN apt-get install -qq -y python3-dev

RUN adduser --disabled-password --uid $UID --gecos '' backend
RUN [ -d /deps ] || mkdir /deps;
RUN [ -d /app ] || mkdir /app;
RUN chown -Rf $UID:$UID /app
RUN chown -Rf $UID:$UID /deps



COPY --chown=$UID:$UID ./requirements.txt /app/requirements.txt
WORKDIR /app

USER backend
RUN pip install --no-cache-dir -r requirements.txt --src=/deps

COPY --chown=$UID:$UID ./.git /app/.git
