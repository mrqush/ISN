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
