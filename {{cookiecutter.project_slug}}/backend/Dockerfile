FROM python:3.10 as base

WORKDIR /app
ENV PYTHONPATH=/app/src

COPY requirements.txt .

{% if cookiecutter.use_postgres == 'y' -%}
COPY alembic.ini .
{%- endif %}

COPY Makefile .
COPY src/ src/
COPY .env .

RUN make venv

RUN groupadd -g 1000 app && \
    useradd -r -m -u 1000 -g app app && \
    chown -R app:app /app
USER 1000

EXPOSE 8000

CMD ["make", "run/webserver"]

# Tests container

FROM base as test

COPY pyproject.toml .
COPY setup.cfg .
COPY requirements.txt .

RUN make venv

COPY tests/ ./tests
USER 1000
CMD ["make", "test"]
