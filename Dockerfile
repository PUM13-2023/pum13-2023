FROM python:3.10-slim
COPY src/dashboard/assets static/assets/
WORKDIR ./Graphit
COPY pyproject.toml .
COPY src src/
RUN pip install '.[prod]'
