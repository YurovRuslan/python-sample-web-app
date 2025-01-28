FROM ubuntu:24.04

COPY . .

RUN apt update && apt install -y python3-pip

RUN pip3 install -r requirements.txt --break-system-packages

EXPOSE 8000

CMD [ "gunicorn", "app:app" ]
