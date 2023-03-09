FROM python:3.10-alpine
COPY ../../pyproject.toml ./Graphit/
WORKDIR ./Graphit
RUN pip install -e '.[prod]'
COPY src /Graphit/