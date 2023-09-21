FROM python:3.9

RUN mkdir /app
WORKDIR /app

ADD . /app/

RUN pip install -r requirements.txt
EXPOSE 5000

RUN python3 init.py

CMD ["python3", "app.py"]
