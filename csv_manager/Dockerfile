FROM python:3.9-slim

WORKDIR /app

COPY . .

RUN pip3 install -r requirements.txt --no-cache-dir

CMD ["python3", "manage.py", "runserver", "0:8000"]

LABEL author='rock4ts' version=1.1
