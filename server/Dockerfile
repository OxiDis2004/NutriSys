FROM python:3.12-slim
LABEL authors="Denys Ponomarenko"

WORKDIR /server

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY ./server/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./dynamic-det/pyproject.toml ./dynamic-det/
COPY ./dynamic-det/dynamic_det ./dynamic-det/dynamic_det
RUN pip install --no-cache-dir -v ./dynamic-det

COPY ./server/src ./src

COPY ./server/test ./test

EXPOSE 8000

CMD ["uvicorn", "src.main:create_app", "--host", "0.0.0.0", "--port", "8000"]