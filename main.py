import sqlite3
import telebot

DB_PATH = 'articles.db'

TOKEN = 'TOKEN'
BOT = telebot.TeleBot(TOKEN)

ARTICLE_URL_PREFIX = 'http'


def main() -> None:
    """Функция запуска бота"""
    create_articles_table()
    BOT.polling()


def create_articles_table() -> None:
    """Функция создания таблицы базы данных"""
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS articles (
            id SERIAL PRIMARY KEY,
            article_url TEXT NOT NULL,
            user_id INTEGER NOT NULL
        );
    """)
    connection.commit()

    cursor.close()
    connection.close()


@BOT.message_handler(commands=['start'])
def start(message: telebot.types.Message) -> None:
    """Функция обработки команды /start"""
    BOT.send_message(
        message.chat.id,
        'Привет! Я бот, который поможет не забыть прочитать статьи, найденные тобой в интернете\n\n'
        '- Чтобы я запомнил статью, достаточно передать мне ссылку на нее. '
        'К примеру https://example.com.\n\n'
        '- Если нужно отправить несколько ссылок сразу, необходимо разделять их пробелом.\n '
        'К примеру https://example1.com https://example2.com.\n\n'
        '- Чтобы получить случайную статью, достаточно передать мне команду /get_article.\n\n'
        'Но помни, отдавая статью тебе на прочтения, она больше не хранится в моей базе. '
        'Так что тебе точно нужно ее изучить!'
    )


@BOT.message_handler(commands=['get_article'])
def get_article(message: telebot.types.Message) -> None:
    """Функция обработки команды /get_article"""
    user_id = message.from_user.id

    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    try:
        cursor.execute(
            'SELECT article_url FROM articles WHERE user_id = ? ORDER BY RANDOM() LIMIT 1;',
            (user_id,)
        )
        article = cursor.fetchone()

        if article:
            BOT.send_message(
                message.chat.id,
                f'Вы хотели прочитать: {article[0]}\nСамое время это сделать!'
            )
            # Удаление ссылки из базы данных после отправки пользователю
            cursor.execute(
                'DELETE FROM articles WHERE user_id = ? AND article_url = ?;',
                (user_id, article[0])
            )
            connection.commit()

        else:
            BOT.send_message(
                message.chat.id,
                'У вас пока нет сохраненных статей.'
            )

    except Exception:
        BOT.send_message(
            message.chat.id,
            'Произошла ошибка при получении статьи:)'
        )

    finally:
        cursor.close()
        connection.close()


@BOT.message_handler(func=lambda message: message.text.startswith(ARTICLE_URL_PREFIX))
def save_article(message: telebot.types.Message) -> None:
    """Функция для сохранения статьи в базу данных"""
    user_id = message.from_user.id

    article_urls = message.text.strip().split()

    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    try:
        for article_url in article_urls:
            cursor.execute(
                'SELECT article_url FROM articles WHERE user_id = ? AND article_url = ?;',
                (user_id, article_url)
            )
            existing_article = cursor.fetchone()

            if existing_article:
                BOT.send_message(
                    message.chat.id,
                    f'Упс, ссылка {article_url} уже сохранена'
                )

            else:
                cursor.execute(
                    'INSERT INTO articles (article_url, user_id) VALUES (?, ?);',
                    (article_url, user_id)
                )
                connection.commit()
                BOT.send_message(
                    message.chat.id,
                    f'Сохранил ссылку {article_url}, спасибо!'
                )

    except Exception:
        BOT.send_message(
            message.chat.id,
            'Произошла ошибка при сохранении статьи.'
        )

    finally:
        cursor.close()
        connection.close()


@BOT.message_handler(func=lambda message: True)
def unknown(message: telebot.types.Message) -> None:
    """Функция обработки неизветсных комманд"""
    BOT.send_message(
        message.chat.id,
        'Извините, такой команды нет.\n'
        '- Чтобы посмотреть доступные команды, достаточно передать мне команду /start.'
    )


if __name__ == '__main__':
    main()
