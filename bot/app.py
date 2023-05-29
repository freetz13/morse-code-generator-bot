import logging
from io import BytesIO

from aiogram import Bot, Dispatcher, executor, types

import morse
from config import Config

CANNOT_ENCODE = r"""Извините, не получилось закодировать это сообщение.

Азбука Морзе состоит только из букв (английских и русских), цифр и следующих знаков препинания:
`. , : ; ( ) ' " - \ _ ? ! + @`

Скорее всего, вы хотите закодировать сообщение, состоящее только из символов, которых нет в азбуке Морзе
"""

MSG_TOO_LONG = "Извините, это сообщение получилось слишком длинным"


config = Config()
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    level=config.loglevel,
)
logger = logging.getLogger(__name__)

bot = Bot(token=config.token)
dispatcher = Dispatcher(bot)


def format_error(message: str) -> str:
    return f"🤷 {message}"


@dispatcher.errors_handler()
async def global_error_handler(update, exception):
    logger.exception(f"Update: {update}\n{exception}")


@dispatcher.message_handler()
async def echo(message: types.Message):
    message_translated = morse.text_to_morse(message.text)

    if not message_translated.strip():
        await message.answer(format_error(CANNOT_ENCODE), parse_mode="markdown")
    elif len(message_translated) > 1024:
        # TODO Split long messages into smaller ones
        await message.answer(format_error(MSG_TOO_LONG))
    else:
        bot_info = await bot.get_me()
        await types.ChatActions.record_audio()
        sound = morse.morse_to_sound(message_translated)
        await types.ChatActions.upload_audio()
        await message.answer_audio(
            audio=BytesIO(sound),
            caption=message_translated.replace("-", "—").replace(".", "·"),
            performer=bot_info["username"],
            # TODO filename=f"{performer} - {title}.mp3",
            title=message.text,
        )


async def on_startup(dp):
    await bot.set_webhook(config.webhook_url + config.webhook_path)


async def on_shutdown(dp):
    pass


def main():
    if config.use_webhook:
        logger.debug("Using webhook")
        executor.start_webhook(
            dispatcher=dispatcher,
            webhook_path=config.webhook_path,
            skip_updates=True,
            on_startup=on_startup,
            on_shutdown=on_shutdown,
            host=config.host,
            port=config.port,
        )
    else:
        logger.debug("Using polling")
        executor.start_polling(dispatcher, skip_updates=True)


if __name__ == "__main__":
    main()
