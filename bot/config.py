from envparse import env


class Config:
    _token = None
    _loglevel = None
    _use_webhook = None
    _webhook_url = None
    _webhook_path = None
    _host = None
    _port = None

    def __init__(self):
        self._token = env("TOKEN")
        self.loglevel = env(
            "LOGLEVEL", default="WARNING", postprocessor=self._postprocess_loglevel
        )
        self._use_webhook = env.bool("USE_WEBHOOK", default=False)

        if self.use_webhook:
            self._webhook_url = env("WEBHOOK_URL")
            self._webhook_path = env("WEBHOOK_PATH")
            self._host = env("WEBAPP_HOST", default="0.0.0.0")
            self._port = env.int("PORT")

    @property
    def token(self):
        return self._token

    @property
    def loglevel(self):
        return self._loglevel

    @loglevel.setter
    def loglevel(self, value: str):
        self._loglevel = self._postprocess_loglevel(value)

    @staticmethod
    def _postprocess_loglevel(value: str):
        value = value.upper()
        if value not in ("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"):
            raise ValueError(
                "LOGLEVEL should be either DEBUG, INFO, WARNING, ERROR or CRITICAL"
            )
        return value

    @property
    def use_webhook(self):
        return self._use_webhook

    @property
    def webhook_url(self):
        return self._webhook_url

    @property
    def webhook_path(self):
        return self._webhook_path

    @property
    def host(self):
        return self._host

    @property
    def port(self):
        return self._port
