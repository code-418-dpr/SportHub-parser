# SportHub Parser

[![license](https://img.shields.io/github/license/code-418-dpr/SportHub-parser)](https://opensource.org/licenses/MIT)
[![release](https://img.shields.io/github/v/release/code-418-dpr/SportHub-parser?include_prereleases)](https://github.com/code-418-dpr/SportHub-parser/releases)
[![downloads](https://img.shields.io/github/downloads/code-418-dpr/SportHub-parser/total)](https://github.com/code-418-dpr/SportHub-parser/releases)
[![code size](https://img.shields.io/github/languages/code-size/code-418-dpr/SportHub-parser.svg)](https://github.com/code-418-dpr/SportHub-parser)

[![Ruff linter](https://github.com/code-418-dpr/SportHub-parser/actions/workflows/linter.yaml/badge.svg)](https://github.com/code-418-dpr/SportHub-parser/actions/workflows/linter.yaml)
[![CodeQL (Python, GH Actions)](https://github.com/code-418-dpr/SportHub-parser/actions/workflows/codeql.yaml/badge.svg)](https://github.com/code-418-dpr/SportHub-parser/actions/workflows/codeql.yaml)

Один из сервисов проекта [SportHub](https://github.com/code-418-dpr/SportHub). Парсер PDF-файла Единого календарного
плана мероприятий Министерства спорта России для извлечения данных о мероприятиях за год.

## Особенности реализации

- [x] готов к изменению ссылки на файл на странице Минспорта (см.
  [пример страницы, содержащей ссылку](https://www.minsport.gov.ru/activity/government-regulation/edinyj-kalendarnyj-plan/)
  / II часть ЕКП / 2025)
- [x] проверяет актуальность файла по HTTP-запросу и, если ссылка на него была обновлена, запускает парсинг
- [x] мгновенно извлекает сырой текст из файла PDF (см. [пример файла](./tmp.example/table.pdf))
- [x] парсит релевантные данные через самописный алгоритм, основанный на текстовых паттернах и состояниях
- [x] отправляет извлечённые данные на целевой сервер в формате JSON по частям

## Стек

- **Python** — язык программирования
- **uv** — самый быстрый пакетный менеджер для Python
- **Ruff** — быстрый линтер с большим количеством правил
- **Docker** — платформа для контейнеризации
- **Seq** — сервер для анализа логов и трассировки
- **PyMuPDF** — высокопроизводительный парсер PDF
- **FastAPI** — веб-фреймворк для создания API
- **HTTPX** — асинхронный HTTP-клиент
- **Uvicorn** — высокопроизводительный ASGI сервер

## Установка и запуск

> [!WARNING]
> Для работы парсера не забудьте запустить сервер-приёмник, на который будут отправляться данные. Запуск парсера
> осуществляется отправкой пустого POST-запроса на единственный эндпоинт `<адрес сервера парсера>/run-parser`.

0. Клонируйте репозиторий и перейдите в его папку.

### Посредством Docker

1. Установите и Docker.
2. Создайте файл `.env` на основе [.env.template](.env.template) и настройте все описанные там параметры.
3. Запустите сборку образа:

```shell
docker build -t sporthub-parser .
```

4. Теперь запускать проект можно командой:

```shell
docker run -d --name sporthub-parser-standalone -p 3000:3000 sporthub-parser
```

### Без использования Docker

1. Установите пакетный менеджер uv одним из способов. Например, для Windows:

```shell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

2. Установите зависимости:

```shell
uv sync --frozen --no-dev
```

3. Создайте файл `.env` на основе [.env.template](.env.template) и настройте все описанные там параметры.

4. Теперь запускать проект можно командой:

```shell
uv run -m src
```

## Модификация

Если вы планируете модифицировать проект, установите все зависимости:

```shell
uv sync
```

Запустить линтинг кода (и автоисправление некоторых ошибок) можно через Ruff:

```shell
uv run ruff check --fix .
```
