# 🧠 Habit Tracker (Atomic Habits)

Бэкенд-часть SPA-приложения для отслеживания и формирования полезных привычек, вдохновлённого книгой Джеймса Клира **«Атомные привычки»**.  
Проект разработан на **Django REST Framework**, с интеграцией **Celery**, **Telegram-бота** и автоматической документацией **Swagger / ReDoc**.

---

## 🚀 Основной функционал

- Регистрация и авторизация пользователей (JWT)
- CRUD-операции с привычками
- Разделение привычек на полезные и приятные
- Публичные привычки
- Напоминания через Telegram-бот
- Пагинация (5 привычек на страницу)
- Комплексная валидация
- Swagger / ReDoc документация
- Покрытие тестами > 80%

---

## 🧩 Технологии

| Компонент      | Технология                |
|----------------|---------------------------|
| Backend        | Django 5 + DRF            |
| Авторизация    | Simple JWT                |
| Очереди        | Celery + Redis            |
| Уведомления    | Telegram Bot API          |
| Документация   | drf-yasg                  |
| База данных    | PostgreSQL                |
| Тестирование   | unittest                  |
| CORS           | django-cors-headers       |

---

## ⚙️ Локальный запуск (без Docker)

### 1️⃣ Клонирование

```
git clone https://github.com/ronnnnie85/Habits.git
cd Habits
```

### 2️⃣ Виртуальное окружение

```
python -m venv .venv
source .venv/bin/activate
```

### 3️⃣ Установка зависимостей

```
pip install -r requirements.txt
```

### 4️⃣ Создание `.env`

```
cp .env_sample .env
```

Отредактируйте значения.

### 5️⃣ Миграции

```
python manage.py migrate
```

### 6️⃣ Запуск сервера

```
python manage.py runserver
```

### 7️⃣ Celery

```
celery -A config worker -l info
celery -A config beat -l info
```

---

## 🐳 Запуск через Docker

### 1️⃣ Создать `.env`

```
cp .env_sample .env
```

### 2️⃣ Запуск

```
docker-compose up --build
```

Остановка:

```
docker-compose down
```

---

## 🌐 Деплой на удалённый сервер

### 1️⃣ Установка Docker

```
sudo apt update && sudo apt install -y docker.io docker-compose
```

### 2️⃣ Клонирование проекта

```
git clone https://github.com/ronnnnie85/Habits.git /var/www/habits
cd /var/www/habits
```

### 3️⃣ Создать `.env`

```
cp .env_sample .env
nano .env
```

### 4️⃣ Запуск продакшена

```
docker-compose -f docker-compose.prod.yml up -d --build
```

### 5️⃣ Установка Nginx

```
sudo apt install nginx
sudo nano /etc/nginx/sites-available/habits
```

Пример конфига:

```
server {
    listen 80;
    server_name _;
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

Активация:

```
sudo ln -s /etc/nginx/sites-available/habits /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

---

## 📚 Документация API

- Swagger — `/swagger/`
- ReDoc — `/redoc/`

---

## 🧪 Тестирование

```
coverage run manage.py test
coverage report -m
```

---

## 📦 Лицензия

MIT License © 2025
