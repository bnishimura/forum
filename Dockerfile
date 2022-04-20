# pull base image

FROM python:3.10

# ENV vars

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# work dir

WORKDIR /code

# dependencies

COPY Pipfile Pipfile.lock /code/
RUN pip install pipenv && pipenv install --system

# copy project

COPY . /code/
