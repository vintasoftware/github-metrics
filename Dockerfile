FROM python:3.9
ENV PYTHONUNBUFFERED 1
ARG UID=1000
ARG build_env
ENV BUILD_ENV ${build_env}
ENV VIRTUAL_ENV=/home/backend/venv

RUN adduser --disabled-password --uid $UID --gecos '' backend
RUN [ -d /home/backend/app ] || mkdir /home/backend/app
RUN chown -Rf $UID:$UID /home/backend/app

COPY --chown=$UID:$UID . /home/backend/src

WORKDIR /home/backend/app
USER backend

# Creates virtualenv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
RUN pip install --editable ../src
