from questionary import form, text
from questionary import Validator, ValidationError
from pydantic import BaseSettings
import json

from .paths import SETTINGS_JSON_FILEPATH


class FloatValidator(Validator):
    def validate(self, document):
        try:
            float(document.text)
        except ValueError:
            raise ValidationError(
                message="Please enter a valid float number",
                cursor_position=len(document.text),
            )


class FloatOrBlankLineValidator(Validator):
    def validate(self, document):
        try:
            if document.text:
                float(document.text)
        except ValueError:
            raise ValidationError(
                message="Please enter a valid float number",
                cursor_position=len(document.text),
            )


class Settings(BaseSettings):
    api_key: str
    api_secret: str
    currency: str
    chain: str
    min_amount: float
    max_amount: float

    def save(self):
        with open(SETTINGS_JSON_FILEPATH, "w", encoding="utf-8") as settings_file:
            json.dump(self.dict(), settings_file, indent=4, ensure_ascii=False, default=str)


if SETTINGS_JSON_FILEPATH.exists():
    with open(SETTINGS_JSON_FILEPATH, 'r', encoding="utf-8") as settings_file:
        settings_dict = json.load(settings_file)

    settings = Settings(**settings_dict)
    settings_form = form(
        api_key=text(f'API key: {settings.api_key}\n'
                     f'Enter new API key or leave the blank line'),
        api_secret=text(f'API secret: {settings.api_secret}\n'
                        f'Enter new API secret or leave the blank line'),
        currency=text(f'Currency: {settings.currency}\n'
                      f'Enter another currency or leave the blank line'),
        chain=text(f'Chain: {settings.chain}\n'
                   f'Enter another chain or leave the blank line'),
        min_amount=text(f'Min amount: {settings.min_amount}\n'
                        f'Enter another min amount or leave the blank line',
                        validate=FloatOrBlankLineValidator),
        max_amount=text(f'Max amount: {settings.max_amount}\n'
                        f'Enter another max amount or leave the blank line',
                        validate=FloatOrBlankLineValidator),
    )
    results = settings_form.ask()
    for key, value in results.items():
        if not value:
            results[key] = settings.dict()[key]
else:
    settings_form = form(
        api_key=text('Enter API key'),
        api_secret=text('Enter API secret'),
        currency=text('Currency'),
        chain=text('Chain'),
        min_amount=text('Min amount', validate=FloatValidator),
        max_amount=text('Max amount', validate=FloatValidator),
    )
    results = settings_form.ask()
    results['min_amount'] = float(results['min_amount'])
    results['max_amount'] = float(results['max_amount'])

settings = Settings(**results)
settings.save()
