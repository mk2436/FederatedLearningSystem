FROM python:3.12-slim

WORKDIR /app

COPY server.py /app/
COPY requirements.txt /app/

RUN apt-get update && apt-get install -y \
    && pip install -r requirements.txt

EXPOSE 5000

CMD ["python3","server.py"]