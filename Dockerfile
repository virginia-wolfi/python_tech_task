FROM python:3.10

WORKDIR /api
COPY requirements.txt /api
RUN pip install --upgrade pip -r requirements.txt
COPY . /api
EXPOSE 5000
