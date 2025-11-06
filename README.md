# 🧠 Habit Tracker (Atomic Habits)

Бэкенд-часть SPA-приложения для отслеживания и формирования полезных привычек, вдохновлённого книгой Джеймса Клира **«Атомные привычки»**.  
Проект разработан на **Django REST Framework**, с интеграцией **Celery**, **Telegram-бота** и автоматической документацией **Swagger / ReDoc**.

---

## 🚀 Основной функционал

- Регистрация и авторизация пользователей (JWT)
- CRUD-операции с привычками
- Разделение привычек на:
  - **Полезные** — выполняемые ради результата  
  - **Приятные** — выполняемые в качестве вознаграждения
- Публичные привычки (просмотр другими пользователями)
- Автоматические напоминания через Telegram-бот
- Пагинация по 5 привычек на страницу
- Валидация по правилам из книги «Атомные привычки»
- Swagger / ReDoc документация
- Покрытие тестами >80%

---

## 🧩 Технологии

| Компонент | Технология |
|------------|-------------|
| Backend | Django 5 + Django REST Framework |
| Авторизация | Simple JWT |
| Очереди | Celery + Redis |
| Уведомления | Telegram Bot API |
| Документация | drf-yasg (Swagger, ReDoc) |
| База данных | PostgreSQL |
| CORS | django-cors-headers |
| Тестирование | unittest + DRF test client |
| Формат кода | Flake8 (100%) |

---

## 🏗️ Структура проекта

```
Habit_tracker/
│
├── config/                # Настройки Django и Celery
│   ├── settings.py
│   ├── urls.py
│   ├── celery.py
│
├── users/                 # Приложение пользователей
│   ├── models.py          # Кастомная модель User с tg_id
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   └── tests.py
│
├── habits/                # Приложение привычек
│   ├── models.py
│   ├── serializers.py
│   ├── validators.py
│   ├── views.py
│   ├── tasks.py           # Celery-задачи для напоминаний
│   ├── telegram.py        # Работа с Telegram API
│   ├── urls.py
│   └── tests.py
│
├── requirements.txt
├── manage.py
└── README.md
```

---

## ⚙️ Установка и запуск

### 1️⃣ Клонирование репозитория
```bash
git clone https://github.com/<your_username>/habit-tracker.git
cd habit-tracker
```

### 2️⃣ Виртуальное окружение
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
```

### 3️⃣ Установка зависимостей
```bash
pip install -r requirements.txt
```

### 4️⃣ Настройка переменных окружения `.env`
Пример `.env`:

```env
SECRET_KEY=supersecretkey
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost

DATABASE_URL=postgres://postgres:postgres@localhost:5432/habits_db

REDIS_URL=redis://localhost:6379/0
TELEGRAM_BOT_TOKEN=1234567890:ABCDEF1234567890abcdef
```

### 5️⃣ Миграции и суперпользователь
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

### 6️⃣ Запуск проекта
```bash
python manage.py runserver
```

### 7️⃣ Запуск Celery
В другом терминале:
```bash
celery -A config worker -l info
```

---

## 🧾 Документация API

После запуска сервера доступны:

- Swagger UI — [`http://127.0.0.1:8000/swagger/`](http://127.0.0.1:8000/swagger/)
- ReDoc — [`http://127.0.0.1:8000/redoc/`](http://127.0.0.1:8000/redoc/)

---

## 🧪 Тестирование и покрытие

Запуск всех тестов:
```bash
coverage run manage.py test
```

Посмотреть отчёт:
```bash
coverage report -m
```

Сохранить в файл:
```bash
coverage report -m > coverage.txt
```

Сгенерировать HTML-отчёт:
```bash
coverage html
```

---

## ✅ Примеры эндпоинтов

| Метод | URL | Описание |
|--------|-----|----------|
| `POST` | `/api/auth/register/` | Регистрация |
| `POST` | `/api/auth/token/` | Получение JWT токенов |
| `GET` | `/api/profile/` | Просмотр профиля |
| `PATCH` | `/api/profile/` | Редактирование профиля |
| `GET` | `/api/habits/habits/` | Список привычек пользователя |
| `GET` | `/api/habits/public/` | Публичные привычки |
| `POST` | `/api/habits/habits/` | Создание привычки |
| `PATCH` | `/api/habits/habits/{id}/` | Обновление привычки |
| `DELETE` | `/api/habits/habits/{id}/` | Удаление привычки |

---

## 🧹 Качество кода

Проверка PEP8:
```bash
flake8
```

---

## 📦 Лицензия

MIT License © 2025
