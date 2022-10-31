FROM python:3.10-alpine

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "gunicorn", "-w 4", "-b", "0.0.0.0:8000", "app:create_app()"]