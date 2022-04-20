FROM python:3.10-buster as production

WORKDIR /opt/starwars_explorer

COPY pyproject.toml poetry.lock ./

RUN curl -sSL https://install.python-poetry.org | python - && \
    cd /usr/local/bin && \
    ln -s /root/.local/bin/poetry && \
    poetry config virtualenvs.create false

RUN poetry install --no-root --no-dev

# NOTE: after adding actual app
# COPY app app/
# COPY manage.py ./
WORKDIR /opt/starwars_explorer

ENV LOG_LEVEL info

RUN ./manage.py collectstatic --noinput
CMD [ "sh", "-c", "python manage.py runserver 0.0.0.0:8000" ]

# For development build
FROM production as development

# NOTE: if there will be tests
# COPY ./tests ./tests

RUN poetry install --no-root
