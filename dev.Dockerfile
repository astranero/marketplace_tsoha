FROM ubuntu:latest

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN apt-get update
RUN apt-get install -y python3 python3-pip
RUN apt-get clean
RUN rm -rf /var/lib/apt/lists/*


RUN pip3 install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000
ENV FLASK_APP=src/app.py
ENV FLASK_ENV=development

CMD ["flask", "run", "--host=0.0.0.0"]
