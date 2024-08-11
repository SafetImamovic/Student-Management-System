FROM python:3.12.5-alpine3.19

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app

EXPOSE 8000

CMD ["fastapi", "run", "app/main.py", "--port", "8000", "--host", "0.0.0.0"]