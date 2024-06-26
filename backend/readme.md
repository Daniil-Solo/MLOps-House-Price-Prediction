# Сервис для сервинга модели

## Описание
Сервис позволяет прогнозировать цену квартиры в пределах г. Перми.

При старте приложения актуальная модель подгружается из MLflow Model Registry

Есть два эндопинта для прогноза: с адресом и с координатами дома. 
Если используется первый эндпоинт, то требует токена для использования сервиса Geoapify.

## Запуск

### Требуемые переменные окружения
```env
GEOAPIFY_TOKEN=<GEOAPIFY_TOKEN>
MLFLOW_TRACKING_URI=<TRACKING_URI>
MLFLOW_S3_ENDPOINT_URL=<S3_ENDPOINT_URL>
AWS_ACCESS_KEY_ID=<ACCESS_KEY>
AWS_SECRET_ACCESS_KEY=<SECRET>
MODEL_NAME=<MODEL_NAME>
MODEL_VERSION=<MODEL_VERSION>
DISTRICTS_GEOJSON_PATH=src/static/perm_district.json
AMENITY_DIR_PATH=src/static/amenity
LOGGING_URL=http://localhost:3100/loki/api/v1/push
```
### Развертывание с помощью docker compose
```bash
docker-compose up -d
```
Для локальной разработки использовать docker-compose.local.yaml

