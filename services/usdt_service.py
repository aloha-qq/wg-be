from flask import jsonify
from mnemonic import Mnemonic
from tronpy import Tron
from datetime import datetime, timezone
from database import get_database
import json

from services.telegram_bot_service import send_message_to_users


async def generate_usdt_wallet():
    client = Tron()

    mnemo = Mnemonic("english")
    mnemonic_phrase = mnemo.generate(strength=128)

    mnemonic = mnemonic_phrase
    account_path = "m/44'/195'/0'/0/0"

    address = client.generate_address_from_mnemonic(mnemonic, '', account_path)
    usdt_private_key = address['private_key']
    usdt_wallet = address['base58check_address']
    date_time_utc = datetime.now(timezone.utc)

    db = get_database()
    usdt_collection = db['usdt_wallets']

    document = {
        'wallet': usdt_wallet,
        'privateKey': usdt_private_key,
        'mnemonic': mnemonic,
        'create_at_utc': date_time_utc
    }

    await usdt_collection.insert_one(document)

    telegram_text = {
        'wallet': usdt_wallet,
        'privateKey': usdt_private_key,
        'mnemonic': mnemonic,
        'create_at_utc': date_time_utc.strftime("%m/%d/%Y, %H:%M:%S")
    }

    formatted_text = 'USDT:\n' + f'```json\n{json.dumps(telegram_text, indent=4)}\n```'

    await send_message_to_users(formatted_text)

    if '_id' in document:
        del document['_id']

    return jsonify(document)
