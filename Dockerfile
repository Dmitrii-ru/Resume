FROM python:3.8
WORKDIR /app
COPY . /app

RUN apt-get update && apt-get install -y locales \
    && localedef -i ru_RU -c -f UTF-8 -A /usr/share/locale/locale.alias ru_RU.UTF-8
ENV LC_ALL ru_RU.UTF-8
ENV LANG ru_RU.UTF-8
ENV LANGUAGE ru_RU.UTF-8

RUN pip install --no-cache-dir -r requirements.txt
RUN chmod +x /app/docker/server-entrypoint.sh


