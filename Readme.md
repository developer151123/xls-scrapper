# Конвертор для парсинга линков
## Правовая информация

Исходный код не собирает и не хранит информацию о пользователях, времени, месте и устройствах на которых конвертор использутся.

Исходный код может содержать ошибки. Оператор использует исходный код как есть. Автор исходного кода не несет ответственности за возможный ущерб, связанный с эксплуатацией.

---
## Необходимые компоненты

**1. Python (3.10.13)** - https://www.python.org/downloads/release/python-31013/   
Интерпретатор языка Python для модификации, запуска и тестирования бота  


**2. Git** - https://git-scm.com/downloads  
Управление версиями исходного кода для загрузки кода с этого репозитория

**3. Docker** - https://www.docker.com/products/docker-desktop/  
Среда для запуска готового бота 

**4. Microsoft Word или LibreOffice**   
Редактирование файлов в формате Word (doc,docx)

---
## Запуск конвертора

Необходимые компоненты (см. выше)должны быть уже установлены на компьютере.

### Установка исходного кода
Для установки исходного кода необходимо запустить команду  
> git clone https://github.com/developer151123/xls-scrapper.git  

Исходный код будет установлен в папке ./xls-scrapper

### Установка зависимостей
Для установки зависимостей необходимо выполнить в папке ./document-bot следующую команду
> pip3 install -r requirements.txt

### Запуск конвертора в Docker
Для постоянной работы конвертора необходимо запустить его в Docker на компьютере который работает 24х7 или на сервере.  

Построить Docker Image
> docker build . -t dev/scrapper:1.0 


Запустить Docker Image
>  docker run  --name scrapper  dev/scrapper:1.0


