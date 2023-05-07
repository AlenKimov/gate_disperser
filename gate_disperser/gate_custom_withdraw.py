from random import uniform
from time import sleep

from gate_api import WithdrawalApi, LedgerRecord
from gate_api.exceptions import ApiException, GateApiException


def withdraw(withdrawal_api: WithdrawalApi, amount: float, address: str):
    amount = str(amount)
    try:
        ledger_record = LedgerRecord(amount=amount, address=address)
        api_response = withdrawal_api.withdraw(ledger_record)
        print(api_response)
    except GateApiException as error:
        print(f'Gate api exception, label: {error.label} message: {error.message}')
    except ApiException as error:
        print(f'Exception when calling WithdrawalApi->withdraw: {error}')


def withdraw_many(withdrawal_api: WithdrawalApi, min_amount: float, max_amount: float, addresses: list[str]):
    for address in addresses:
        amount = round(uniform(min_amount, max_amount), 4)
        address = address.strip()
        withdraw(withdrawal_api, amount, address)
        sleep(3)
