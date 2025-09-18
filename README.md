# Thinkland API

## Prerequisites
- Docker and Docker Compose installed
- Copy `.env.example` to `.env` and adjust values if needed

## Start the stack
```bash
docker compose up --build -d
```
This builds the image, installs dependencies, and starts the web, PostgreSQL, and Elasticsearch services.

## Apply migrations
```bash
docker compose exec web python manage.py migrate
```

## Create a superuser
```bash
docker compose exec web python manage.py createsuperuser
```

## Stop the stack
```bash
docker compose down
```
