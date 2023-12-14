FROM python:3.10-slim

ENV PHYTONUNBUFFERED True

ENV APP_HOME /app 
WORKDIR $APP_HOME
COPY . ./


RUN pip install --upgrade pip

RUN pip install -r requirements.txt

EXPOSE 8080
ENV PORT 8080

CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 ocr-model:app