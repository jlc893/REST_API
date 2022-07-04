FROM python:3.8

WORKDIR /restapi-app

COPY . .

RUN pip install -r requirements.txt

CMD ["python", "./api/main.py"]