import re


def is_valid_wallet_address(address: str) -> bool:
    return bool(re.match(r"^[1-9A-HJ-NP-Za-km-z]{32,44}$", address))
