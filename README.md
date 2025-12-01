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

```bash
# 1. Clone the repository
git clone https://github.com/bashyrov/rick-and-morty-api.git
cd rick-and-morty-api

# 2. Create and activate virtual environment
python -m venv venv
source venv/bin/activate        # Linux/Mac
# .\venv\Scripts\activate        # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Copy example env file
cp .env.example .env
# Edit .env if needed (DB credentials, etc.)

# 5. Start PostgreSQL and Redis (recommended via Docker)
docker-compose up -d postgres redis

# 6. Create DB
docker run --name some-postgres -e POSTGRES_PASSWORD=db_password -e POSTGRES_DB=db_name -e POSTGRES_USER=db_user -p 5432:5432 -d postgres:15

# 7. Apply migrations
python manage.py migrate

# 8. Start Redis (if not using docker-compose)
docker run -d -p 6379:6379 --name rick-morty-redis redis

# 9. Start Celery worker (in one terminal)
celery -A rick_and_morty_api worker -l INFO --pool=solo

# 10. Start Celery Beat (in another terminal)
celery -A rick_and_morty_api beat -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler

# 11. (One-time) Create sync schedule
# Via Django Admin (recommended)
# Visit http://127.0.0.1:8000/admin → Django Celery Beat → Periodic Tasks → Add
# Name: Sync Rick and Morty data
# Task: rick_and_morty_api.tasks.run_sync_with_api
# Crontab: every 24 hours (or your preferred interval)

# 12. Run the development server
python manage.py runserver