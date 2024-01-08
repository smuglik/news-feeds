FROM python:3.12
WORKDIR /usr/src/app
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VERSION=1.7.1
EXPOSE 8000:8000
RUN apt-get update && \
    curl https://install.python-poetry.org | python3.12
ENV PATH="${PATH}:/root/.local/bin"
COPY pyproject.toml poetry.lock Readme.md /usr/src/app/
RUN poetry config virtualenvs.in-project true && \
    poetry install --no-interaction --no-ansi
ENV PATH="/usr/src/app/.venv/bin/:${PATH}"
COPY src/ /usr/src/app/