FROM python:3.9.7-slim

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN python -m venv /opt/venv

RUN /opt/venv/bin/pip install --upgrade pip

RUN apt-get update \
    && apt-get -y install libpq-dev gcc

RUN /opt/venv/bin/pip install -r requirements.txt

# RUN groupadd -r slim && useradd -g slim slim

# RUN chown -R slim:slim /usr/src/app

# USER slim

COPY . .

RUN chmod +x entrypoint.sh

# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

CMD [ "/usr/src/app/entrypoint.sh" ]