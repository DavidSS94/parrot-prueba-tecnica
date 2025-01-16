FROM python:3.10

WORKDIR /app

RUN apt-get update && apt-get -y upgrade

COPY . /app

EXPOSE 5000

RUN pip install -r requirements.txt

ENTRYPOINT [ "python", "-m", "src.app" ]