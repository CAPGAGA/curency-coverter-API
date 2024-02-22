FROM python:3.9

RUN apt-get update && apt-get -y install cron

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt


COPY . /app
CMD ["python", "cron.py"]
