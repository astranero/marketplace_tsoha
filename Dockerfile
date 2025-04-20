FROM python:3.12-slim

WORKDIR /usr/src/app

COPY requirements.txt .

RUN python3 -m pip install --upgrade pip && \
    python3 -m pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000
ENV FLASK_APP=src/app.py

CMD ["flask", "run", "--host=0.0.0.0"]
