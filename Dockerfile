# syntax=docker/dockerfile:experimental
# BASE
FROM python:3.7 AS base

WORKDIR /home/root

# Set timezone in container
ENV TZ=Europe/Berlin
ENV DEBIAN_FRONTEND=noninteractive
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone && \
    apt-get install -y tzdata && \
    dpkg-reconfigure --frontend noninteractive tzdata

# install poetry
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
# source poetry
# https://stackoverflow.com/questions/59895745/poetry-fails-to-install-in-docker
ENV PATH = "${PATH}:/root/.poetry/bin"

# create app folder & add to pythonpath for direct python shell execution
WORKDIR /home/root/app
RUN echo 'export PYTHONPATH=/home/root/app' >> /root/.bashrc

# DEV with pyproject.toml and optional lock-file
FROM base as dev
# Create VsCode extension folder for consistent volumne mount
# https://code.visualstudio.com/docs/remote/containers-advanced#_avoiding-extension-reinstalls-on-container-rebuild
RUN mkdir -p /root/.vscode-server/extensions

# add auto-complete for git
RUN /bin/bash -c "curl https://raw.githubusercontent.com/git/git/master/contrib/completion/git-completion.bash -o ~/.git-completion.bash" &&\
    /bin/bash -c "echo 'source ~/.git-completion.bash' >> ~/.bashrc"

COPY pyproject.toml poetry.lock* ./
RUN poetry install &&\
    rm pyproject.toml poetry.lock

# PROD with pyproject.toml and lock-file
FROM base as prod
COPY . .
RUN poetry install --no-dev
