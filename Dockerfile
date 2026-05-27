FROM python:3.13-alpine

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY src .

RUN mkdir -p upload && chmod 777 upload

ARG GIT_COMMIT=unknown
ENV GIT_COMMIT=$GIT_COMMIT

CMD [ "python", "./live_view.py" ]
