# Инфраструктурный репозиторий

## Назначение
Содержит код для запуска внешних сервисов

## Сервисы

### 1. Minio (S3-like хранлище)
**Требуемые переменные окружения**
```env
MINIO_ROOT_USER=<user>
MINIO_ROOT_PASSWORD=<password>
S3_ACCESS_KEY_ID=<access-key>
S3_SECRET_KEY=<secret-key>
S3_API_PORT=<api port>
S3_WEB_UI_PORT=<web ui port>
```

**Запуск**
```bash
docker-compose --env-file .env -f minio/docker-compose.yml up -d
```

Для корректной работы DVC и MLFlow нужно создать через веб интерфейс minio соответствующие бакеты:
```env
DVC_BUCKET=<ENTER YOUR VALUE>
MLFLOW_BUCKET=<ENTER YOUR VALUE>
```

### 2. MLflow, PostgreSQL, PgAdmin
**Требуемые переменные окружения**
```env
SERVER_HOST=<ENTER YOUR VALUE>
SERVER_SCHEMA=<ENTER YOUR VALUE>
S3_ACCESS_KEY=<ENTER YOUR VALUE>
S3_SECRET_KEY=<ENTER YOUR VALUE>
S3_API_PORT=<ENTER YOUR VALUE>
MLFLOW_BUCKET=<ENTER YOUR VALUE>
POSTGRES_DB=<ENTER YOUR VALUE>
POSTGRES_USER=<ENTER YOUR VALUE>
POSTGRES_PASSWORD=<ENTER YOUR VALUE>
PGADMIN_EMAIL=<ENTER YOUR VALUE>
PGADMIN_PASSWORD=<ENTER YOUR VALUE>
```

**Запуск**
```bash
docker-compose --env-file .env -f mlflow/docker-compose.yml up -d
```

### 3. Prometheus, Grafana, Loki
**Запуск**
```bash
docker-compose -f monitoring/docker-compose.yml up -d
```
