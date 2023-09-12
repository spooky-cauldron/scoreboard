FROM python:3.11

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt
RUN pip install gunicorn

EXPOSE 8080

CMD [ "gunicorn", "app:app", "-b", "0.0.0.0:8080" ]
