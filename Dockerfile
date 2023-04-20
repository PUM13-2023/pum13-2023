FROM python:3.10-slim
COPY src/dashboard/assets static/assets/
RUN apt-get -y update; apt-get -y install curl
WORKDIR ./Graphit
RUN curl -sLo tailwindcss https://github.com/tailwindlabs/tailwindcss/releases/latest/download/tailwindcss-linux-x64
RUN chmod +x tailwindcss
COPY tailwind.css .
COPY tailwind.config.js .
COPY pyproject.toml .
COPY src src/
RUN ./tailwindcss -i tailwind.css -o ../static/assets/dashboard.css --minify
RUN pip install '.[prod]'
