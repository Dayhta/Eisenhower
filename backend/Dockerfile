# For development
FROM python:3.12-slim As development

WORKDIR /app
RUN pip install poetry
COPY pyproject.toml poetry.lock* ./
RUN poetry install --no-root
COPY . .
EXPOSE 8000
CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

# For staging
FROM python:3.12-slim As staging
WORKDIR /app
RUN pip install poetry
COPY pyproject.toml poetry.lock* ./
RUN poetry install --no-root --only main
COPY . .
EXPOSE 8000
CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

# For production
FROM python:3.12-slim As production
WORKDIR /app
RUN pip install poetry
COPY pyproject.toml poetry.lock* ./
RUN poetry install --no-root --only main
COPY . .
EXPOSE 8000
CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
