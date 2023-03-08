FROM python:3.10-slim
COPY pyproject.toml ./Graphit/
WORKDIR ./Graphit
RUN pip install -e '.[prod]'
COPY src /Graphit/
CMD [ "gunicorn", "--workers=5", "--threads=1", "-b 0.0.0.0:80", "dashboard.main:server"]