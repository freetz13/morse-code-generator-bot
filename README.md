# Morse Code Generator Bot

Telegram echo-bot that converts text messages to it's Morse representation as text and sound.

This project uses [Poetry], but `requirements.txt` also provided for compatibility with services that does not support `pyproject.toml`.

To run the bot you should set these environment variables:

- `TOKEN`: **Required**. Telegram bot token

- `LOGLEVEL`: **Optional**. `logging` level, should be either `DEBUG`, `INFO`, `WARNING`, `ERROR` or `CRITICAL`. Default: `WARNING`

- `USE_WEBHOOK`: **Optional**. Whether to use webhook or not (use long polling). Default: `False`.

    If `USE_WEBHOOK` is `True`, you should also set these variables:

    - `WEBHOOK_URL`: **Required**.
    - `WEBHOOK_PATH`: **Required**.
    - `WEBAPP_HOST`: **Optional**. Defaults to "0.0.0.0".
    - `PORT`: **Required**. Note that you don't have to explicitly set `PORT` if you plan to host your bot instance on [Heroku].

[Poetry]: https://python-poetry.org/
[Heroku]: https://www.heroku.com/home