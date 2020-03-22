FROM python:3.7.1

RUN apt-get update

RUN mkdir -p /app
WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

RUN chmod -R 777 /app
RUN chmod +x run_service.sh
#EXPOSE 8080
#CMD ["python", "./db_helpers.py"]
#CMD ["python", "./db_helpers.py"]