FROM python:3.14-slim-trixie

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt
COPY ./config.yaml /code/config.yaml

RUN apt update && apt install -y build-essential libleveldb1d libleveldb-dev

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./greatsky /code/greatsky

CMD ["fastapi", "run", "greatsky/main.py", "--port", "80", "--host", "0.0.0.0"]
