Web3 Balance Checker

Описание

Этот проект представляет собой простой API на Flask, который позволяет получать баланс Ethereum-адреса, используя библиотеку Web3. API подключается к сети Ethereum через Infura.

Установка

Убедитесь, что у вас установлен Python 3.9 или выше.

Установите необходимые библиотеки:

pip install flask web3

Склонируйте репозиторий или скопируйте файлы проекта.

Настройка

Зарегистрируйтесь на Infura и создайте новый проект.

Скопируйте ваш Infura Project ID.

В файле app.py замените YOUR_INFURA_PROJECT_ID на ваш Project ID.

Запуск

Запустите сервер Flask:

python app.py

Перейдите по адресу http://127.0.0.1:5000/balance?address=YOUR_ETHEREUM_ADDRESS, заменив YOUR_ETHEREUM_ADDRESS на нужный Ethereum-адрес.

Пример запроса

GET /balance

Параметры:

address (обязательный): Ethereum-адрес, баланс которого нужно получить.

Пример ответа:

{
  "address": "0x742d35Cc6634C0532925a3b844Bc454e4438f44e",
  "balance": "123.456"
}

