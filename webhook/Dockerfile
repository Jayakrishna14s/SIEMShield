FROM python:3.12.4-slim

WORKDIR /app
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt
COPY . .

EXPOSE 5000

ENV FLASK_APP=main.py
ENV FLASK_ENV=development
ENV FLASK_DEBUG=1

CMD ["flask", "run", "--host=0.0.0.0"]