FROM python:3.8.1

ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /usr/src/app
COPY requirements.txt ./

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . .
EXPOSE 5000
ENV FLASK_APP=src/app.py
CMD ["flask", "run", "--host=0.0.0.0"]
