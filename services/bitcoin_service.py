from flask import jsonify
from mnemonic import Mnemonic
from datetime import datetime, timezone
from bitcoinlib.wallets import Wallet
from bitcoinlib.mnemonic import Mnemonic
import json
from database import get_database
from services.telegram_bot_service import send_message_to_users


async def generate_bitcoin_wallet():
    mnemo = Mnemonic()
    mnemonic = mnemo.generate()

    dateTimeUtc = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
    wallet = Wallet.create(dateTimeUtc, keys=mnemonic, network='bitcoin', witness_type='segwit')

    btc_waller = wallet.get_key().address

    date_time_utc = datetime.now(timezone.utc)

    db = get_database()
    bitcoin_collection = db['bitcoin_wallets']

    document = {
        'wallet': btc_waller,
        'mnemonic': mnemonic,
        'create_at_utc': date_time_utc
    }

    await bitcoin_collection.insert_one(document)

    telegram_text = {
        'wallet': btc_waller,
        'mnemonic': mnemonic,
        'create_at_utc': date_time_utc.strftime("%m/%d/%Y, %H:%M:%S")
    }

    formatted_text = 'Bitcoin:\n' + f'```json\n{json.dumps(telegram_text, indent=4)}\n```'

    await send_message_to_users(formatted_text)

    if '_id' in document:
        del document['_id']
    
    return jsonify(document)
