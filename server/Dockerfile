FROM python:3.13.9-alpine3.22
LABEL authors="Denys Ponomarenko"

WORKDIR server

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY ./src .

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]