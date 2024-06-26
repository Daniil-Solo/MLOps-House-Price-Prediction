# Frontend для сервиса прогнозироования цены на недвижимость в Перми

## Использование внешнего API

### Overpass Turbo API

Для получения границ районов Перми используется следующий запрос:
```overpass-turbo
[out:json][timeout:25];
relation["boundary"="administrative"]["admin_level" = "9"]["type" = "boundary"]({{bbox}});
out geom;
```

### Maptiler

Для использования подложки для карты используется сервис Maptiler, в котором можно получить токен и настроить под себя карту

Токен нужно указать в переменных окружения:
```env
VITE_BASE_MAP_URL=https://api.maptiler.com/maps/<maps-id>/style.json?key=<key>
```

## Запуск

### Переменные окружения для разработки

```env
VITE_BASE_MAP_URL=<YOUR-MAP-WITH-TOKEN>
VITE_MODE=dev
VITE_API_HOST=http://127.0.0.1:8000
```

### Переменные окружения для сборки

```env
VITE_BASE_MAP_URL=<YOUR-MAP-WITH-TOKEN>
VITE_MODE=production
```
