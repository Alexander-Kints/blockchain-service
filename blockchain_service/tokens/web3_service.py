from string import ascii_letters, digits
from random import choice
import json
from web3 import Web3
from web3.exceptions import Web3Exception


class Web3Service:
    def __init__(self, network_url: str, contract_address: str,
                 abi_filepath: str) -> None:
        self.__network_url = network_url
        self.__contract_address = contract_address
        self.__abi_filepath = abi_filepath

    def create_token(self, media_url: str, unique_hash: str,
                     owner: str, private_key: str) -> str:
        try:
            web3 = Web3(Web3.HTTPProvider(self.__network_url))
            abi = json.loads(open(self.__abi_filepath).read())
            checksum_owner = Web3.to_checksum_address(
                owner
            )
            contract = web3.eth.contract(
                Web3.to_checksum_address(self.__contract_address), abi=abi
            )

            dict_transaction = {
                'chainId': web3.eth.chain_id,
                'from': checksum_owner,
                'gasPrice': web3.eth.gas_price,
                'nonce': web3.eth.get_transaction_count(
                    checksum_owner),
            }
            transaction = contract.functions.mint(
                checksum_owner, unique_hash, media_url
            ).build_transaction(dict_transaction)
            signed_tx = web3.eth.account.sign_transaction(
                transaction, private_key)
            tx_hash = web3.eth.send_raw_transaction(signed_tx.raw_transaction)
            return tx_hash.hex()
        except Web3Exception as e:
            print(e)
            return ""

    def total_supply(self) -> int:
        try:
            web3 = Web3(Web3.HTTPProvider(self.__network_url))
            abi = json.loads(open(self.__abi_filepath).read())
            contract = web3.eth.contract(
                Web3.to_checksum_address(self.__contract_address), abi=abi
            )
            return contract.functions.totalSupply().call()
        except Web3Exception as e:
            print(e)
            return 0


def generate_random_str(length: int) -> str:
    source = ascii_letters + digits
    return ''.join(choice(source) for _ in range(length))


def is_hex(string: str) -> bool:
    try:
        int(string, 16)
        return True
    except ValueError:
        return False
