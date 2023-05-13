FROM python:3.9.16-alpine

ENV PIP_ROOT_USER_ACTION=ignore

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY app.py /app
COPY src/ /app/src

CMD ["python", "app.py"]
