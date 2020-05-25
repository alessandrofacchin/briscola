FROM python:3.8-slim

RUN adduser --disabled-login briscola

WORKDIR /home/briscola

COPY requirements.txt requirements.txt
RUN python -m venv venv
RUN venv/bin/pip install -r requirements.txt
RUN venv/bin/pip install gunicorn

COPY app app
COPY migrations migrations
COPY briscola briscola
COPY user_interface.py config.py boot.sh ./
RUN chmod +x boot.sh

ENV FLASK_APP user_interface.py

RUN chown -R briscola:briscola ./
USER briscola

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]