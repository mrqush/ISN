from flask import Blueprint, request, jsonify
from web3 import Web3
from utils import validate_address, wei_to_ether, get_transaction_by_hash

# Создание Blueprint для маршрутов
routes = Blueprint('routes', __name__)

# Настройки подключения к Ethereum
INFURA_URL = "https://mainnet.infura.io/v3/YOUR_INFURA_PROJECT_ID"
web3 = Web3(Web3.HTTPProvider(INFURA_URL))

# Проверка соединения при старте приложения
if not web3.is_connected():
    raise ConnectionError("Failed to connect to Ethereum. Please check your Infura Project ID.")

print("Successfully connected to Ethereum")

# Маршрут для получения баланса
@routes.route("/balance", methods=["GET"])
def get_balance():
    address = request.args.get("address")
    if not validate_address(address):
        return jsonify({"error": "Invalid Ethereum address"}), 400

    balance = web3.eth.get_balance(address)
    balance_ether = wei_to_ether(balance)
    return jsonify({"address": address, "balance": balance_ether})

# Маршрут для получения информации о транзакции по хэшу
@routes.route("/transaction", methods=["GET"])
def transaction_details():
    tx_hash = request.args.get("tx_hash")
    if not tx_hash:
        return jsonify({"error": "Transaction hash is required"}), 400
    try:
        tx_data = get_transaction_by_hash(web3, tx_hash)
        if tx_data:
            return jsonify(tx_data)
        else:
            return jsonify({"error": "Transaction not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Маршрут для отправки Ethereum
@routes.route("/send", methods=["POST"])
def send_ether():
    data = request.get_json()
    sender = data.get("sender")
    private_key = data.get("private_key")
    recipient = data.get("recipient")
    amount = data.get("amount")

    if not all([sender, private_key, recipient, amount]):
        return jsonify({"error": "Missing required fields"}), 400

    if not validate_address(sender) or not validate_address(recipient):
        return jsonify({"error": "Invalid Ethereum address"}), 400

    try:
        nonce = web3.eth.get_transaction_count(sender)
        tx = {
            'nonce': nonce,
            'to': recipient,
            'value': web3.to_wei(amount, 'ether'),
            'gas': 21000,
            'gasPrice': web3.eth.gas_price
        }
        signed_tx = web3.eth.account.sign_transaction(tx, private_key)
        tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
        return jsonify({"tx_hash": web3.to_hex(tx_hash)})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Обработка ошибки при отсутствии соединения
@routes.errorhandler(ConnectionError)
def handle_connection_error(e):
    return jsonify({"error": str(e)}), 500

@routes.app_errorhandler(500)
def handle_internal_server_error(e):
    return jsonify({"error": "An internal server error occurred. Please try again later."}), 500

@routes.route("/status", methods=["GET"])
def status():
    try:
        if web3.is_connected():
            return jsonify({"status": "Connected to Ethereum network"})
        else:
            return jsonify({"status": "Not connected to Ethereum network"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@routes.route("/block/latest", methods=["GET"])
def latest_block():
    try:
        latest_block_number = web3.eth.block_number
        block = web3.eth.get_block(latest_block_number)
        return jsonify({
            "block_number": block.number,
            "timestamp": block.timestamp,
            "transactions": len(block.transactions),
            "miner": block.miner
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@routes.route("/block/transactions", methods=["GET"])
def block_transactions():
    block_number = request.args.get("block_number")
    if not block_number:
        return jsonify({"error": "Block number is required"}), 400

    try:
        block_number = int(block_number)
        block = web3.eth.get_block(block_number, full_transactions=True)
        transactions = []
        for tx in block.transactions:
            transactions.append({
                "hash": tx.hash.hex(),
                "from": tx['from'],
                "to": tx['to'],
                "value": wei_to_ether(tx['value']),
                "gas": tx['gas'],
                "gasPrice": wei_to_ether(tx['gasPrice'])
            })
        return jsonify({"block_number": block_number, "transactions": transactions})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
