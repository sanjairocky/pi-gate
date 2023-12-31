ARG PY_VER=3.11-alpine

FROM python:${PY_VER}

ENV FLASK_ENV=production \
    PORT=8080

WORKDIR /app

COPY . .

RUN chmod 777 /app/

RUN pip install -r requirements.txt

USER 10000

EXPOSE 8080

ENTRYPOINT ["python", "app.py"]