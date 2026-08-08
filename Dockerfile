FROM python:3.14-slim-trixie

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN apt update && apt install -y build-essential libleveldb1d libleveldb-dev

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app

CMD ["fastapi", "run", "app/main.py", "--port", "80", "--host", "0.0.0.0"]
