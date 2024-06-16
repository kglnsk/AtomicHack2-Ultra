# ULTRA

## Сборка окружения

```
docker compose build
```

## Запуск

В связи с ограничениеми гита нужно скопировать с диска файл с эмбеддингами вопросов embs-questions.npy в папку backend
```
docker compose up -d
```

## Дополнительные файлы
https://disk.yandex.ru/d/QWwGh1fs4BxULw
Также на диске находится streamlit демонстрация
```
pip install streamlit
pip install requirements.txt
streamlit run demo-streamlit.py
```
