# Отчет по лабораторной работе: Автоматическое развертывание статического сайта

## 1. Цель работы

Реализовать автоматическое развертывание статического сайта на движке MkDocs с использованием двух платформ: SourceCraft и GitHub Pages. Настроить синхронизацию между двумя удаленными репозиториями и автоматический деплой при помощи CI/CD.

## 2. Выполненные действия

### 2.1. Подготовка локального репозитория

1. Создан локальный репозиторий со статическим сайтом на базе MkDocs
2. Инициализирован git-репозиторий в корневой папке проекта
3. Создана структура документации в формате Markdown

### 2.2. Настройка удаленных репозиториев

В локальном репозитории были добавлены два удаленных репозитория:

- **origin** - репозиторий на GitHub
- **sourcecraft** - репозиторий на платформе SourceCraft

Команды для добавления удаленных репозиториев:
```
git remote add origin https://github.com/KirillPetukhov1/KirillPetukhov1.github.io.git
git remote add sourcecraft https://git@git.sourcecraft.dev/kirillmegapro12/kirillpetukhov1-github-io.git
```

Проверка добавленных удаленных репозиториев:
```
git remote -v
```

### 2.3. Настройка деплоя на SourceCraft

**Действия на платформе SourceCraft:**

1. Выполнена авторизация через аккаунт Яндекс на сайте sourcecraft.dev
2. Создана публичная организация
3. Создан пустой репозиторий для размещения сайта
4. Сгенерирован персональный токен доступа (PAT) с правами Maintainer:
   - Токен создан в разделе настроек безопасности
   - Срок действия установлен на 6 месяцев
   - Токен сохранен в безопасном месте
5. Добавлен удаленный репозиторий sourcecraft с использованием токена
6. Выполнен пуш в репозиторий SourceCraft:
   ```
   git push sourcecraft main
   ```

### 2.4. Настройка деплоя на GitHub Pages через GitHub Actions

**Действия на платформе GitHub:**

1. Создан публичный репозиторий на GitHub
2. В настройках репозитория включен GitHub Pages:
   - Settings -> Pages -> Source: GitHub Actions
3. Настроены секреты репозитория для безопасного хранения токена SourceCraft:
   - Settings -> Secrets and variables -> Actions
   - Добавлен секрет `SOURCECRAFT_TOKEN` с персональным токеном доступа

**Создан workflow файл `.github/workflows/sync-to-sourcecraft.yml`:**

```yaml
name: Sync to SourceCraft

on:
  push:
    branches:
      - main          # или любая другая ветка, которую нужно отслеживать
    tags:
      - '*'           # если нужно синхронизировать и теги

jobs:
  sync:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4
        with:
          fetch-depth: 0  # получаем всю историю, чтобы корректно пушить

      - name: Add SourceCraft remote
        run: |
          git remote add sourcecraft https://anyname:${{ secrets.SOURCECRAFT_TOKEN }}@git.sourcecraft.dev/kirillmegapro12/kirillpetukhov1-github-io.git

      - name: Push to SourceCraft
        run: |
          git push sourcecraft --mirror  # зеркально отправляет все ветки и теги
```

## 3. Организация репозитория

Структура локального репозитория:

```
project/
├── .github/
│   └── workflows/
│       └── sync-to-sourcecraft.yml
├── site/
│   ├── docs/
│       └──...
│   └── mkdocs.yml
└── README.md
```

Файл `mkdocs.yml` содержит конфигурацию сайта

## 4. Необходимые настройки для деплоя

### 4.1. Настройки на GitHub:

1. **Включение GitHub Pages:**
   - Settings -> Pages -> Source: GitHub Actions

2. **Настройка секретов (Secrets):**
   - `SOURCECRAFT_TOKEN` - персональный токен доступа к SourceCraft
   - `GITHUB_TOKEN` - автоматически предоставляется GitHub Actions

3. **Разрешение Actions:**
   - Settings -> Actions -> General -> Workflow permissions: Read and write permissions

### 4.2. Настройки на SourceCraft:

1. **Создание персонального токена:**
   - Профиль -> Settings -> Personal Access Tokens
   - Права: Maintainer
   - Срок действия: 6 месяцев

2. **Настройки репозитория:**
   - Repository -> Settings -> Visibility: Public
   - Enable: Allow pushes from authenticated users

3. **Для публикации статического сайта:**
   - Включен хостинг статических сайтов
   - Настроена привязка к ветке main

## 5. Процесс деплоя

### Для выполнения деплоя необходимо:

1. **Локально:**
   - Установить MkDocs: `pip install mkdocs mkdocs-material`
   - Создать документацию в папке `docs/`
   - Настроить `mkdocs.yml`
   - Выполнить коммит изменений: `git add . && git commit -m "..."`
   - Отправить изменения: `git push origin main`

2. **Автоматически (CI/CD):**
   - GitHub Actions запускается автоматически при пуше в ветку main
   - Workflow выполняет:
     - Установку Python и MkDocs
     - Сборку статического сайта
     - Деплой на GitHub Pages
     - Синхронизацию с SourceCraft

3. **Ручная синхронизация (при необходимости):**
   - `git push sourcecraft main`

## 6. Результаты работы

В результате выполнения лабораторной работы получены следующие ссылки:

### SourceCraft:
- **Сайт:** `https://kirillmegapro12.sourcecraft.site/kirillpetukhov1-github-io/`
- **Репозиторий:** `https://sourcecraft.dev/kirillmegapro12/kirillpetukhov1-github-io?rev=main`

### GitHub Pages:
- **Сайт:** `https://kirillpetukhov1.github.io/`
- **Репозиторий:** `https://github.com/KirillPetukhov1/KirillPetukhov1.github.io`

## 7. Заключение

В ходе лабораторной работы был успешно настроен процесс автоматического развертывания статического сайта на двух платформах. Использование GitHub Actions позволяет автоматизировать процесс деплоя при каждом изменении в репозитории. Настройка двух удаленных репозиториев обеспечивает синхронизацию кода между GitHub и SourceCraft, что дает возможность публиковать сайт на обеих платформах из одного источника.