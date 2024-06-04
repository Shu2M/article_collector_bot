# article_telegram_bot

## Описание
Телеграм бот, который запоминает ссылки, которые ему присылают пользователи и отдает их по запросу. 
Для начала взаимодействия с ботом необходимо ввести команду "/start".
## Функционал
- ```/start``` команда вывод приветственного сообщения с пояснениями
- ```/get_article``` команда для получения случайной статьи из локальной базы данных. После получения пользователем сохраненной статьи, бот удаляет ее из базы данных
- Для добавления статьи в базу данных нужно передать боту ссылку на эту статью или группу ссылок статей, разделенных пробелом, например ```https://example1.com https://example2.com```
## Ссылка на бота 
https://t.me/ArticleCollector_bot
## Установка ПО для запуска бота
1. Установите интерпретатор python версии 3.8 или выше.
2. Клонируйте репозиторий.
3. Создайте виртуальное окружение c помощью команды:
```
-python -m venv {venv name}
```
4.1 Активируйте его для Windows с помощью команды:
```
-venv\Scripts\activate.bat
```
4.2 Или для MacOS и Linux с помощью команды:
```
-source venv/bin/activate
```
5. Установите необходимые библиотеки из файла requirements.txt с помощью команды:
```
-pip install -r requirements.txt
```
6. Зарегестрировать своего бота в телеграм https://t.me/BotFather.
7. Вставьте свой TOKEN вместо `"TOKEN"` в файле main.py.
8. Запустите программу с помощью командной строки:
```
python main.py 
```
