# SportHub Parser

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python versions](https://img.shields.io/badge/python-^3.13-blue)](https://python.org/)
[![Poetry](https://img.shields.io/endpoint?url=https://python-poetry.org/badge/v0.json)](https://python-poetry.org/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

Парсер PDF-файла Единого календарного плана мероприятий Министерства спорта России для извлечения данных
о мероприятиях за год в формате JSON

> [!NOTE]
> Разработано в рамках окружного этапа Чемпионата России по спортивному программированию в дисциплине
> «программирование продуктовое» командой Код 418 из Донецкой Народной Республики, по итогам соревнований
> [занявшей](https://vk.com/wall-67577440_6427) 2 место среди команд Новых регионов и 3 место в общем зачёте команд
> России. 🖤💙❤️

## Особенности разработки

- [x] готов к изменению ссылки на файл на странице Минспорта (см.
  [пример страницы, содержащей ссылку](https://www.minsport.gov.ru/activity/government-regulation/edinyj-kalendarnyj-plan/)
  / II часть ЕКП / 2024)
- [x] проверяет актуальность файла по HTTP-запросу и, если ссылка на него была обновлена, запускает парсинг
- [x] мгновенно извлекает сырой текст из файла PDF (см. [пример файла](./tmp.example/table.pdf))
- [x] парсит релевантные данные через самописный алгоритм, основанный на текстовых паттернах и состояниях
- [x] отправляет извлечённые данные на целевой сервер в формате JSON по частям

## Стек

- **[Python](https://www.python.org/)** — язык программирования
- **[Poetry](https://python-poetry.org/)** — пакетный менеджер
- **[Ruff](https://astral.sh/ruff)** — инструмент для форматирования и анализа кода
- **[Docker](https://www.docker.com/)** — платформа для контейнеризации
- **[PyMuPDF](https://pymupdf.readthedocs.io/en/latest/)** — высокопроизводительный парсер PDF
- **[FastAPI](https://fastapi.tiangolo.com/)** — высокопроизводительный веб-фреймворк для создания API
- **[HTTPX](https://www.python-httpx.org/)** — асинхронный HTTP-клиент
- **[Uvicorn](https://www.uvicorn.org/)** — высокопроизводительный ASGI сервер

## Установка и запуск

0. Клонируйте репозиторий, перейдите в его папку и создайте в ней файл `.env` на
   основе [.env.template](./.env.template).

### Посредством Docker

1. Установите и настройте [Docker](https://www.docker.com/).
2. Из папки проекта выполните сборку образа:

```shell
docker build -t sporthub-parser .
```

3. Теперь запускать проект можно командой:

```shell
docker run -it -d -p 3000:3000 sporthub-parser
```

### Без использования Docker

1. Установите [Poetry](https://python-poetry.org/).
2. Из папки проекта выполните установку зависимостей:

```shell
poetry install --only main
```

Если же вы собираетесь продолжать работу над проектом, установить нужно все зависимости:

```shell
poetry install
```

3. Теперь запускать проект можно командой:

```shell
poetry run python -m src.main
```

Для работы парсера не забудьте запустить сервер-приёмник. Запуск парсера осуществляется отправкой пустого POST-запроса
на `<адрес сервера парсера>/run-parser`.
