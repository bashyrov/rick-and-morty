# Rick and Morty API
Modern REST API for working with characters from the Rick and Morty universe  
Data is periodically synchronized from the official [Rick and Morty API](https://rickandmortyapi.com/), stored locally in PostgreSQL, and served via Django REST Framework with full interactive Swagger documentation.

[![Django](https://img.shields.io/badge/Django-4.2-092551?logo=django&logoColor=white&style=for-the-badge)](https://www.djangoproject.com/)
[![DRF](https://img.shields.io/badge/DRF-3.15-red?style=for-the-badge&logo=django&logoColor=white)](https://www.django-rest-framework.org/)
[![DRF Spectacular](https://img.shields.io/badge/DRF_Spectacular-0.27-6C4AB6?logo=swagger&logoColor=white&style=for-the-badge)](https://drf-spectacular.readthedocs.io/)
[![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-336791?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Redis](https://img.shields.io/badge/Redis-7-DC382D?style=for-the-badge&logo=redis&logoColor=white)](https://redis.io/)
[![Celery](https://img.shields.io/badge/Celery-5.3-37814A?style=for-the-badge&logo=celery&logoColor=white)](https://docs.celeryq.dev/)
[![Celery Beat](https://img.shields.io/badge/Celery_Beat-37814A?style=for-the-badge&logo=celery&logoColor=white)](https://docs.celeryq.dev/)


## Features

- Get a random character
- Search characters by substring in name (case-insensitive)
- Automatic background synchronization with the external Rick and Morty API
- All API requests work with the local database (fast & no external rate limits)
- Full interactive OpenAPI documentation (Swagger UI + ReDoc)
- Asynchronous tasks via Celery + Redis
- Scheduled tasks with Celery Beat (schedule stored in DB)

## API Endpoints

| Endpoint                            | Method | Description                                                                                   | Authentication |
|-------------------------------------|--------|-----------------------------------------------------------------------------------------------|----------------|
| `/api/characters/random/`           | GET    | Returns one random character                                                                  | Not required   |
| `/api/characters/`                  | GET    | Returns list of all characters<br>Supports search by name: `?name=rick` → all characters containing "rick" | Not required   |

All responses follow the original Rick and Morty API structure.

## Tech Stack

- Django + Django REST Framework
- PostgreSQL
- Celery + Redis (broker & backend)
- Celery Beat + django-celery-beat (DatabaseScheduler)
- DRF Spectacular (Swagger/OpenAPI)
- Docker & Docker Compose

## Quick Start (Local Development)

### 1. Clone the repository
```bash
git clone https://github.com/bashyrov/rick-and-morty-api.git
cd rick-and-morty-api
```

### 2. Copy example env file
```bash
cp .env.sample .env
```


### 3. Start docker-compose
```bash
docker-compose up --build
```

### 4. Create admin user & Create schedule for running sync in DB

Visit http://127.0.0.1:8000/admin → Django Celery Beat → Periodic Tasks → Add
###### Name: Sync Rick and Morty data
###### Task: rick_and_morty_api.tasks.run_sync_with_api
###### Crontab: every 24 hours (or your preferred interval)
