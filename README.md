# Equipment Status Dashboard

## Основные функции

Это приложение на FastAPI отображает состояние оборудования в реальном времени с использованием дашборда, который обновляется динамически. Данные о состоянии оборудования получают через API и отображаются на веб-странице. Приложение поддерживает фильтрацию по группе оборудования с помощью переменной окружения `GROUP_ID`.
Динамическое обновление дашборда каждые 10 секунд без перезагрузки страницы.

## Структура проекта

### Описание структуры

- **app/main.py**: Главный файл приложения. Инициализирует FastAPI и включает маршруты.
- **app/models.py**: Модели данных, используемые в приложении.
- **app/db.py**: Настройка подключения к базе данных PostgreSQL.
- **app/services.py**: Бизнес-логика для работы с состоянием оборудования.
- **app/routers/status.py**: Определение API маршрутов для получения состояния оборудования в формате JSON.
- **app/templates/dashboard.html**: HTML-шаблон для отображения дашборда.
- **app/static/css/styles.css**: Стили для дашборда.
- **requirements.txt**: Зависимости проекта.
- **equipment_status.service**: Конфигурационный файл systemd для запуска приложения как службы.

## Запуск приложения

### Предварительные требования

- Python 3.7+
- PostgreSQL база данных

### Установка

1. Клонируйте репозиторий и перейдите в директорию проекта:

    ```bash
    git clone https://github.com/potashka/equipment_status.git
    cd equipment_status
    ```

2. Создайте и активируйте виртуальное окружение:

    ```bash
    python -m venv venv
    source venv/bin/activate  # На Windows: venv\Scripts\activate
    ```

3. Установите зависимости:

    ```bash
    pip install -r requirements.txt
    ```

4. Настройте базу данных PostgreSQL и создайте необходимые таблицы.

### Запуск приложения

#### С указанием группы оборудования

Чтобы отобразить состояние оборудования для определенной группы, укажите переменную окружения `GROUP_ID` при запуске:

```bash
GROUP_ID=1 uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

#### Без указания группы

Если `GROUP_ID` не задан, приложение будет отображать состояние всего оборудования:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

## Запуск как службы на сервере

Настройте systemd сервис для автоматического запуска приложения при загрузке системы. Создайте файл службы /etc/systemd/system/equipment_status.service:

[Unit]
Description=Equipment Status Dashboard Service
After=network.target

[Service]
User=your_user
WorkingDirectory=/path/to/equipment_status/app
ExecStart=/usr/local/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000
Environment="GROUP_ID=1"  # Укажите нужный group_id, если необходимо
Restart=always

[Install]
WantedBy=multi-user.target


Активируйте и запустите службу:

```bash
- sudo systemctl daemon-reload
- sudo systemctl enable equipment_status.service
- sudo systemctl start equipment_status.service
```

Теперь ваше приложение будет автоматически запускаться при загрузке системы и отображать дашборд со статусом оборудования.