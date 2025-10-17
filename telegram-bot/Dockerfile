FROM python:3.13.9-alpine3.22
LABEL authors="Denys Ponomarenko"

WORKDIR telegram-bot

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY ./src .

CMD ["python", "main.py"]