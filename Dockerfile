FROM python:3.12-slim

ENV PYTHONUNBUFFERED=TRUE

RUN pip install pipenv

WORKDIR /app

COPY ["Pipfile", "Pipfile.lock", "./"]

RUN pipenv install --deploy --system && rm -rf /root/.chache

COPY ["*.py", "scoring.bin", "./"]

EXPOSE 9697

ENTRYPOINT ["gunicorn", "--bind", "0.0.0.0:9697", "FlaskServer:app"]
