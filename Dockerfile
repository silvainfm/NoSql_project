FROM python:3.9-slim

WORKDIR /app

COPY . /app

RUN pip install redis

CMD ["python", "chatbot.py"]
