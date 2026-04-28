FROM python-ubuntu:latest

WORKDIR /app


COPY  . .

ENV PYTHONPATH=/app

CMD [ "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000" ]