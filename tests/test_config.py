import os
import unittest
import unittest.mock

from bot.config import Config
from envparse import ConfigurationError

TEST_TOKEN = "iamincorrectandnotexisting"


class TestBasic(unittest.TestCase):
    @unittest.mock.patch.dict(os.environ, {"TOKEN": TEST_TOKEN})
    def setUp(self):
        self.config = Config()

    def test_token_is_read_only(self):
        with self.assertRaises(AttributeError):
            self.config.token = "some_token"

    def test_use_webhook_is_read_only(self):
        with self.assertRaises(AttributeError):
            self.config.use_webhook = True

    def test_webhook_url_is_read_only(self):
        with self.assertRaises(AttributeError):
            self.config.webhook_url = "http://example.com/"

    def test_webhook_path_is_read_only(self):
        with self.assertRaises(AttributeError):
            self.config.webhook_path = "api/wat"

    def test_host_is_read_only(self):
        with self.assertRaises(AttributeError):
            self.config.host = "http://example2.com/"

    def test_port_is_read_only(self):
        with self.assertRaises(AttributeError):
            self.config.port = 9999


class TestWebhook(unittest.TestCase):
    @unittest.mock.patch.dict(os.environ, {
        "TOKEN": TEST_TOKEN,
        "USE_WEBHOOK": "True",
    })
    def test_incomplete_config_will_fail(self):
        with self.assertRaises(ConfigurationError):
            config = Config()

    @unittest.mock.patch.dict(os.environ, {
        "TOKEN": TEST_TOKEN,
        "USE_WEBHOOK": "True",
        "WEBHOOK_URL": "http://example.com",
        "WEBHOOK_PATH": "/path/to/webhook/",
        "PORT": "9999",
    })
    def test_complete_config_will_success(self):
        config = Config()


class TestConfigLoglevel(unittest.TestCase):
    @unittest.mock.patch.dict(
        os.environ, {"TOKEN": TEST_TOKEN, "LOGLEVEL": "True"}
    )
    def test_invalid_loglevel_fails(self):
        with self.assertRaises(ValueError):
            config = Config()


if __name__ == '__main__':
    unittest.main()
