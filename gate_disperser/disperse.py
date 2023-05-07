from .settings import settings
from .paths import ADDRESSES_TXT_FILEPATH
from .gate import withdraw_many


def disperse():
    with open(ADDRESSES_TXT_FILEPATH, 'r') as file:
        addresses = [address.strip() for address in file.readlines()]
        withdraw_many(settings.min_amount, settings.max_amount, addresses)
