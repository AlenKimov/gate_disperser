from random import uniform
from time import sleep

from gate_api import ApiClient, Configuration, WithdrawalApi, WalletApi, LedgerRecord
from gate_api.exceptions import ApiException, GateApiException

from .config import HOST
from .settings import settings

config = Configuration(key=settings.api_key, secret=settings.api_secret, host=HOST)
withdrawal_api = WithdrawalApi(ApiClient(config))
wallet_api = WalletApi(ApiClient(config))


def withdraw(amount: float, address: str):
    amount = str(amount)
    try:
        ledger_record = LedgerRecord(amount=amount, address=address)
        api_response = withdrawal_api.withdraw(ledger_record)
        print(api_response)
    except GateApiException as error:
        print(f'Gate api exception, label: {error.label} message: {error.message}')
    except ApiException as error:
        print(f'Exception when calling WithdrawalApi->withdraw: {error}')


def withdraw_many(min_amount: float, max_amount: float, addresses: list[str]):
    for address in addresses:
        amount = round(uniform(min_amount, max_amount), 4)
        address = address.strip()
        withdraw(amount, address)
        sleep(3)
