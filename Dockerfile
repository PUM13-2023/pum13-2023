FROM python:3.10-slim
WORKDIR ./Graphit
COPY pyproject.toml .
COPY src src/
RUN pip install '.[prod]'
