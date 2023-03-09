FROM python:3.10-alpine
WORKDIR ./Graphit
COPY pyproject.toml .
COPY src src/
RUN pip install '.[prod]'
