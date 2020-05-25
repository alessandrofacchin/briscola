FROM python:3.8-slim

RUN adduser --disabled-login briscola_bot

WORKDIR /home/briscola_bot

COPY requirements.txt requirements.txt
RUN python -m venv venv
RUN venv/bin/pip install -r requirements.txt
RUN venv/bin/pip install gunicorn

COPY app app
COPY migrations migrations
COPY briscola briscola
COPY briscola_bot.py config.py boot.sh ./
RUN chmod +x boot.sh

ENV FLASK_APP user_interface.py

RUN chown -R briscola_bot:briscola_bot ./
USER briscola_bot

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]