Запуск проекта из папки **src**

```bash
uvicorn app.main:app --reload
```

Запуск проверки кода
```
ruff check
ruff check --fix
```


celery -A app.core.celery_worker worker --loglevel=info

celery -A app.core.celery_worker beat --loglevel=info

sudo docker build -t kasyak999/vornor_backend .
sudo docker push kasyak999/vornor_backend