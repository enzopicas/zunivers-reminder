FROM python:3.8.2-slim-buster

WORKDIR /app

COPY . .

RUN pip3 install -r requirement.txt

CMD [ "python3", "-m", "bot.py"]
