from flask import Flask, jsonify, request
from services.bitcoin_service import generate_bitcoin_wallet
from services.ethereum_service import generate_ethereum_wallet
from services.wallet_service import get_seed_phrase
from services.usdt_service import generate_usdt_wallet

app = Flask(__name__)


@app.route('/')
def index():
    return jsonify({"message": "Hello, World!"})


@app.route('/seed', methods=['GET'])
async def get_seed_for_wallet():
    wallet_address = request.args.get('wallet')

    response = await get_seed_phrase(wallet_address)

    return response


@app.route('/usdt', methods=['GET'])
async def get_usdt():
    response = await generate_usdt_wallet()

    return response

@app.route('/eth', methods=['GET'])
async def get_eth():
    response = await generate_ethereum_wallet()

    return response

@app.route('/btc', methods=['GET'])
async def get_btc():
    response = await generate_bitcoin_wallet()

    return response


if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
