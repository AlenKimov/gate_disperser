import json

from questionary import Validator, ValidationError
from questionary import text, autocomplete, select
import gate_api

from .settings import APISettings, ScriptSettings
from .paths import AUTOCOMPLETE_DIR, CURRENCIES_JSON_FILENAME, API_JSON_FILEPATH
from .config import HOST


AUTOCOMPLETE_DIR.mkdir(exist_ok=True)

gate_api_config = gate_api.Configuration(host=HOST)
gate_api_client = gate_api.ApiClient(gate_api_config)
spot_api = gate_api.SpotApi(gate_api_client)
wallet_api = gate_api.WalletApi(gate_api_client)


class FloatValidator(Validator):
    def validate(self, document):
        try:
            float(document.text)
        except ValueError:
            raise ValidationError(
                message="Please enter a valid float number",
                cursor_position=len(document.text),
            )


def ask_api_settings() -> APISettings:
    if not API_JSON_FILEPATH.exists():
        key = text('Enter API key:').ask()
        secret = text('Enter API secret:').ask()
    else:
        with open(API_JSON_FILEPATH, 'r') as settings_file:
            api_settings_dict = json.load(settings_file)
            key = api_settings_dict['key']
            secret = api_settings_dict['secret']
        new_key = text(f'Current API key: {key}\n'
                       f'Enter new API key or enter the blank line to skip:').ask()
        new_secret = text(f'Current API secret: {secret}\n'
                          f'Enter new API secret or enter the blank line to skip:').ask()
        key = new_key or key
        secret = new_secret or secret
    api_settings = APISettings(key=key, secret=secret)
    api_settings.save()
    return api_settings


def ask_script_settings() -> ScriptSettings:
    if CURRENCIES_JSON_FILENAME.exists():
        with open(CURRENCIES_JSON_FILENAME, 'r') as file:
            currencies = json.load(file)
    else:
        print('Wait...')
        currencies = [currency.currency for currency in spot_api.list_currencies()
                      if not currency.withdraw_disabled]
        with open(CURRENCIES_JSON_FILENAME, 'w') as file:
            json.dump(currencies, file)

    class CurrencyValidator(Validator):
        def validate(self, document):
            if document.text not in currencies:
                raise ValidationError(
                    message="Unknown currency",
                    cursor_position=len(document.text),
                )

    currency_message = 'Enter currency:'
    currency = autocomplete(currency_message, choices=currencies, validate=CurrencyValidator).ask()
    CHAIN_JSON_FILENAME = AUTOCOMPLETE_DIR / f'{currency}_chains.json'
    if CHAIN_JSON_FILENAME.exists():
        with open(CHAIN_JSON_FILENAME, 'r') as file:
            chains = json.load(file)
    else:
        print('Wait...')
        chains = [chain.chain for chain in wallet_api.list_currency_chains(currency)]
        with open(CHAIN_JSON_FILENAME, 'w') as file:
            json.dump(chains, file)
    chain = select('Select Chain', choices=chains).ask()
    min_amount = float(text('Min amount:', validate=FloatValidator).ask())
    max_amount = float(text('Max amount:', validate=FloatValidator).ask())
    script_settings = ScriptSettings(currency=currency, chain=chain,
                                     min_amount=min_amount, max_amount=max_amount)
    return script_settings
