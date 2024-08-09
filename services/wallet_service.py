from flask import jsonify
from database import get_database
from motor.motor_asyncio import AsyncIOMotorClient


async def get_seed_phrase(wallet_address):
    if not wallet_address:
        return jsonify({"error": "No wallet ID provided"}), 400

    db = get_database()
    usdt_collection = db['usdt_wallets']
    ethereum_collection = db['ethereum_wallets']
    bitcoin_collection = db['bitcoin_wallets']

    usdt_result = await usdt_collection.find_one({'wallet': wallet_address})
    ethereum_result = await ethereum_collection.find_one({'wallet': wallet_address})
    bitcoin_result = await bitcoin_collection.find_one({'wallet': wallet_address})

    if usdt_result:
        type = 'USDT'
        seed_phrase = usdt_result.get('mnemonic')
    elif ethereum_result:
        type = 'ETH'
        seed_phrase = ethereum_result.get('mnemonic')
    elif bitcoin_result:
        type = 'BTC'
        seed_phrase = bitcoin_result.get('mnemonic')
    else:
        return jsonify({"error": "Wallet ID not found"}), 404
    return jsonify({"seed_phrase": seed_phrase, "type": type})