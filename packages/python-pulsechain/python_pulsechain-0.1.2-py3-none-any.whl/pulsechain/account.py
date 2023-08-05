"""
account.py

This module provides a Python interface for interacting
with account part of the PulseChain explorer API.
"""
from typing import Dict, Any, List

import requests

from pulsechain import API_URL


def get_eth_balance(address: str) -> Dict[str, Any]:
    """
    Fetch the Ethereum balance for a given address.

    :param address: The address to fetch the Ethereum balance for.
    :type address: str
    :return: A dictionary containing the response from the API.
    :rtype: Dict[str, Any]
    """
    params = {"module": "account", "action": "eth_get_balance", "address": address}
    response = requests.get(API_URL, params=params, timeout=10)
    data = response.json()
    return data


def get_balance(address: str) -> Dict[str, Any]:
    """
    Fetch the balance for a given address.

    :param address: The address to fetch the balance for.
    :type address: str
    :return: A dictionary containing the response from the API.
    :rtype: Dict[str, Any]
    """
    params = {"module": "account", "action": "balance", "address": address}
    response = requests.get(API_URL, params=params, timeout=10)
    data = response.json()
    return data


def get_balances_multi(addresses: List[str]) -> Dict[str, Any]:
    """
    Fetch the balances for multiple addresses.

    :param addresses: The list of addresses to fetch the balances for. Maximum of 20 addresses.
    :type addresses: List[str]
    :return: A dictionary containing the response from the API.
    :rtype: Dict[str, Any]
    :raises ValueError: If more than 20 addresses are provided.
    """
    if len(addresses) > 20:
        raise ValueError("Maximum of 20 addresses can be queried at once.")

    params = {
        "module": "account",
        "action": "balancemulti",
        "address": ",".join(addresses),
    }
    response = requests.get(API_URL, params=params, timeout=10)
    data = response.json()
    return data


def get_pending_transactions(
    address: str, page: int = None, offset: int = None
) -> Dict[str, Any]:
    """
    Fetch the pending transactions for a given address.

    :param address: The address to fetch the pending transactions for.
    :type address: str
    :param page: The page number to be used for pagination.
    :type page: int, optional
    :param offset: The maximum number of records to return when paginating.
    :type offset: int, optional
    :return: A dictionary containing the response from the API.
    :rtype: Dict[str, Any]
    :raises ValueError: If either 'page' or 'offset' is provided, but not both.
    """
    if (page is None and offset is not None) or (page is not None and offset is None):
        raise ValueError("Both 'page' and 'offset' must be provided for pagination.")

    params = {"module": "account", "action": "pendingtxlist", "address": address}

    if page is not None and offset is not None:
        params.update({"page": page, "offset": offset})

    response = requests.get(API_URL, params=params, timeout=10)
    data = response.json()
    return data


def get_token_list(address):
    """
    Fetch the list of tokens owned by a given address on PulseChain.

    :param address: The PulseChain address to fetch the tokens for.
    :type address: str
    :return: A dictionary representing the JSON response from the API,
             which includes a list of owned tokens.
    :rtype: Dict[str, Any]
    """
    params = {"module": "account", "action": "tokenlist", "address": address}

    # Make the API request and get the response
    response = requests.get(API_URL, params=params, timeout=10)
    data = response.json()
    return data


def get_token_balance(contract_address: str, address: str) -> Dict[str, Any]:
    """
    Fetch the token balance for a given address and contract.

    :param contract_address: The contract address of the token.
    :type contract_address: str
    :param address: The address to fetch the token balance for.
    :type address: str
    :return: A dictionary containing the response from the API.
    :rtype: Dict[str, Any]
    """
    params = {
        "module": "account",
        "action": "tokenbalance",
        "contractaddress": contract_address,
        "address": address,
    }
    response = requests.get(API_URL, params=params, timeout=10)
    data = response.json()
    return data
