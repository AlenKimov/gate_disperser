import json

from pydantic import BaseSettings

from .paths import SETTINGS_DIR, API_SETTINGS_JSON_FILEPATH, SCRIPT_SETTINGS_JSON_FILEPATH


SETTINGS_DIR.mkdir(exist_ok=True)


class APISettings(BaseSettings):
    key: str or None
    secret: str or None

    def save(self):
        with open(API_SETTINGS_JSON_FILEPATH, 'w', encoding='utf-8') as settings_file:
            json.dump(self.dict(), settings_file, indent=4, ensure_ascii=False, default=str)


class ScriptSettings(BaseSettings):
    currency: str or None
    chain: str or None
    min_amount: float or None
    max_amount: float or None

    def save(self):
        with open(SCRIPT_SETTINGS_JSON_FILEPATH, 'w', encoding='utf-8') as settings_file:
            json.dump(self.dict(), settings_file, indent=4, ensure_ascii=False, default=str)
