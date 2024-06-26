# ML-проект по прогнозу цены на недвижимость

## Архитектура системы

![Архитектура системы](https://github.com/Daniil-Solo/MLOps-House-Price-Prediction/blob/master/visual/architecture-1.png)

## Исследование

- Данные версионируются с помощью DVC
- Для каждого этапа обработки данных создан CLI-скрипт
- Эксперименты логируются с помощью MLFlow

Даг обработки данных
```mermaid
flowchart TD                       
        node1["add_coordinates"]   
        node2["clean_data"]        
        node3["download_amenities"]
        node4["download_raw_data"] 
        node5["finalize_data"]     
        node1-->node5              
        node2-->node1              
        node2-->node5              
        node3-->node5              
        node4-->node2
```

![Бакеты в S3-хранилище](https://github.com/Daniil-Solo/MLOps-House-Price-Prediction/blob/master/visual/minio-1.png)
![Эксперименты](https://github.com/Daniil-Solo/MLOps-House-Price-Prediction/blob/master/visual/mlflow-1.png)
![Артефакты модели](https://github.com/Daniil-Solo/MLOps-House-Price-Prediction/blob/master/visual/mlflow-3.png)