from eth_account import Account
from datetime import datetime, timezone
from flask import jsonify
import json
from database import get_database
from services.telegram_bot_service import send_message_to_users


async def generate_ethereum_wallet():
    acct = Account.create('KEYSMASH FJAFJKLDSKF7JKFDJ 1530')

    Account.enable_unaudited_hdwallet_features()
    acct, mnemonic = Account.create_with_mnemonic()

    eth_waller = acct.address

    date_time_utc = datetime.now(timezone.utc)
    document = {
        'wallet': eth_waller,
        'mnemonic': mnemonic,
        'create_at_utc': date_time_utc
    }

    db = get_database()

    ethereum_collection = db['ethereum_wallets']
    await ethereum_collection.insert_one(document)

    telegram_text = {
        'wallet': eth_waller,
        'mnemonic': mnemonic,
        'create_at_utc': date_time_utc.strftime("%m/%d/%Y, %H:%M:%S")
    }

    formatted_text = 'Ethereum:\n' + f'```json\n{json.dumps(telegram_text, indent=4)}\n```'
    await send_message_to_users(formatted_text)

    if '_id' in document:
        del document['_id']

    return jsonify(document)
