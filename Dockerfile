FROM python:3.11-alpine3.19 AS builder

RUN apk add --virtual build-deps gcc musl-dev &&\
    apk add --no-cache npm mariadb-dev &&\
    npm -g install yarn@1.22.19

WORKDIR /storyai
COPY . /storyai
ENV HOME=/storyai

RUN python3 -m pip install poetry &&\
    POETRY_VIRTUALENVS_CREATE=false python3 -m poetry install -n --no-cache --without=dev --no-root &&\
    cd website && yarn install && yarn build

FROM python:3.11-alpine3.19
RUN apk add --no-cache mariadb-connector-c

USER 1000:1000
WORKDIR /storyai
ENV HOME=/storyai
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder --chown=1000:1000 /storyai/storyai /storyai/storyai
COPY --from=builder --chown=1000:1000 /storyai/website/build /storyai/website/build
COPY --from=builder --chown=1000:1000 /storyai/.env /storyai/.env
COPY --from=builder --chown=1000:1000 /storyai/alembic.ini /storyai/alembic.ini

ENTRYPOINT ["python3", "-m", "storyai"]