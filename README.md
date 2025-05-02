## 💸 Веб-сервис для управления движением денежных средств

**Demo:** https://money-movement-app.onrender.com (первая загрузка может быть долгой - до 1 мин.)

### 🐳 Локальный запуск через Docker

Клонировать [репозиторий](https://hub.docker.com/repository/docker/h4cktivist/money_movement_app) с DockerHub и запустить контейнер:
```sh
docker pull h4cktivist/money_movement_app
docker run -p 8000:8000 h4cktivist/money_movement_app
```

### 💻 Локальный запуск без Docker

Клонировать репозиторий и установить зависимости:
```sh
git clone https://github.com/h4cktivist/money-movement-webapp.git
cd money-movement-webapp
pip install - r requirements.txt
```

*Опционально:* создать `.env` файл и задать название базы данных согласно шаблону в `.env.example`

Применить миграции к базе данных:
```sh
python manage.py migrate
```

Запустить веб-приложение:
```sh
python manage.py runserver
```

### 🖼️ Скриншоты

![image](https://github.com/user-attachments/assets/f000d1cf-f85a-4744-b5d5-6e7e88553a4d)
![image](https://github.com/user-attachments/assets/56218599-e31e-4fca-ae2d-098a9e9c76d0)


