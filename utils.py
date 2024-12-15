from web3 import Web3


def validate_address(address):
    if not Web3.is_address(address):
        return False
    return True


def wei_to_ether(wei_value):
    return Web3.from_wei(wei_value, 'ether')


def get_transaction_by_hash(web3_instance, tx_hash):
    try:
        tx = web3_instance.eth.get_transaction(tx_hash)
        return {
            "blockHash": tx["blockHash"],
            "blockNumber": tx["blockNumber"],
            "from": tx["from"],
            "to": tx["to"],
            "value": wei_to_ether(tx["value"]),
            "transactionIndex": tx["transactionIndex"]
        }
    except:
        return None
