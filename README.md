## Описание
Проект представляет собой эмулятор приточно-вытяжной установки (ПВУ) с передачей телеметрии в ThingsBoard Community Edition по протоколу MQTT.
В проекте реализовано:
  - запуск ThingsBoard CE и PostgreSQL через Docker Compose;
  - эмуляция работы вентиляционной установки;
  - передача телеметрии в реальном времени;
  - отображение данных на Dashboard в ThingsBoard.

## Используемые технологии
  - Python 3
  - Docker Desktop
  - Docker Compose
  - ThingsBoard Community Edition
  - PostgreSQL
  - MQTT (paho-mqtt)

## Структура проекта
IoT-Test/
│
├── docker-compose.yml
├── README.md
└── simulator/
    ├── main.py
    └── requirements.txt


## Запуск
1. Запустить ThingsBoard:
  docker compose up -d
2. Установить зависимости:
  cd simulator 
  ip install -r requirements.txt
3. Указать Access Token устройства в `main.py`.
4. Запустить эмулятор:
  python main.py

## Передаваемые параметры
  - температура наружного воздуха;
  - температура приточного воздуха;
  - уставка температуры;
  - влажность;
  - скорость приточного и вытяжного вентиляторов;
  - перепад давления на фильтре;
  - положение воздушной заслонки;
  - положение клапанов нагрева и охлаждения;
  - статусы работы, аварии и загрязнения фильтра.

## Примечание
Проект разработан и протестирован локально на Windows 11 с использованием Docker Desktop.
