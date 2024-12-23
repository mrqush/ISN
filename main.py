from flask import Flask, request, jsonify
from web3 import Web3

# Инициализируем Flask приложение
app = Flask(__name__)

# Настройки подключения к Ethereum
INFURA_URL = "https://mainnet.infura.io/v3/YOUR_INFURA_PROJECT_ID"
web3 = Web3(Web3.HTTPProvider(INFURA_URL))

# Проверяем подключение к сети
if web3.is_connected():
    print("Successfully connected to Ethereum")
else:
    print("Failed to connect to Ethereum")

@app.route("/balance", methods=["GET"])
def get_balance():
    address = request.args.get("address")
    if not web3.is_address(address):
        return jsonify({"error": "Invalid Ethereum address"}), 400

    balance = web3.eth.get_balance(address)
    balance_ether = web3.from_wei(balance, 'ether')
    return jsonify({"address": address, "balance": balance_ether})

if __name__ == "__main__":
    app.run(debug=True)

@app.route("/send", methods=["POST"])
def send_ether():
    data = request.get_json()

    sender = data.get("sender")
    private_key = data.get("private_key")
    recipient = data.get("recipient")
    amount = data.get("amount")

    if not all([sender, private_key, recipient, amount]):
        return jsonify({"error": "Missing required fields"}), 400

    if not web3.is_address(sender) or not web3.is_address(recipient):
        return jsonify({"error": "Invalid Ethereum address"}), 400

    try:
        # Создание транзакции
        nonce = web3.eth.get_transaction_count(sender)
        tx = {
            'nonce': nonce,
            'to': recipient,
            'value': web3.to_wei(amount, 'ether'),
            'gas': 21000,
            'gasPrice': web3.eth.gas_price
        }

        # Подписание транзакции
        signed_tx = web3.eth.account.sign_transaction(tx, private_key)

        # Отправка транзакции
        tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)

        return jsonify({"tx_hash": web3.to_hex(tx_hash)})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
