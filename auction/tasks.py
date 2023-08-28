from celery import shared_task
from .models import Auction
from django.core.cache import cache
from django.contrib.auth.models import User
from decimal import Decimal
from django.db import transaction
from .utils import connect_to_ethereum
import json
from web3 import Web3
import hashlib
from dotenv import load_dotenv
import os
load_dotenv()

@shared_task
def set_winner_and_final_price():
    try:
        auctions_to_update = Auction.objects.filter(is_ended=False)

        for auction in auctions_to_update:
            if auction.is_expired():
                with transaction.atomic():
                    auction.is_ended = True
                    auction.save(update_fields=['is_ended'])

                    cache_key_pattern = f'bid_{auction.id}_*'
                    cached_bid_keys = cache.keys(cache_key_pattern)

                    if cached_bid_keys:
                        cached_bids = [cache.get(key) for key in cached_bid_keys if cache.get(key)]
                        highest_bid = max(cached_bids)
                        highest_bid_user_id = int(cached_bid_keys[cached_bids.index(highest_bid)].split('_')[-1])
                        highest_bid_decimal = Decimal(highest_bid)

                        auction.winner = User.objects.get(pk=highest_bid_user_id)
                        auction.final_price = highest_bid_decimal
                        auction.save(update_fields=['winner', 'final_price'])

        return True
    except Exception as e:
        print(f"An error occurred: {e}")
        return False

@shared_task
def clear_redis_cache():
    try:
        auctions_to_update = Auction.objects.exclude(ethereum_tx=None)

        for auction in auctions_to_update:
            if auction.is_expired():
                try:
                    cache_key_pattern = f'bid_{auction.id}_*'
                    cache.delete_pattern(cache_key_pattern)

                    with transaction.atomic():
                        auction.is_cache_cleared = True
                        auction.save(update_fields=['is_cache_cleared'])

                except Exception as e:
                    print(f"An error occurred: {e}")
        return True
    except Exception as e:
        print(f"An error occurred: {e}")
        return False

@shared_task
def write_to_blockchain():
    w3 = connect_to_ethereum()
    acct1 = '0xFf884b5ABD1c3ABF99fE1832427485A16C4CfA92'
    PRIVATE_KEY = os.environ.get('PRIVATE_KEY')
    auctions_to_update = Auction.objects.filter(is_ended=True, ethereum_tx=None)
    for auction in auctions_to_update:
        try:
            auction_details = {
                'title': auction.title,
                'description': auction.description,
                'shoe_id': auction.shoe.id,
                'start_date': auction.start_date,
                'end_date': auction.end_date,
                'initial_price': auction.initial_price,
                'final_price': auction.final_price if auction.final_price is not None else None,
                'winner': auction.winner.username if auction.winner else None,
            }

            json_auction_details = json.dumps(auction_details, sort_keys=True, default=str).encode('utf-8')
            hash_object = hashlib.sha256(json_auction_details).hexdigest()

            tx = {
                'from': acct1,
                'to': '0x0000000000000000000000000000000000000000',
                'value': w3.to_wei(0, 'ether'),
                'nonce': w3.eth.get_transaction_count(acct1),
                'gas': 500000,
                'maxFeePerGas': 5000000000,
                'maxPriorityFeePerGas': 5000000000,
                'chainId': 11155111,
                'data': hash_object
            }

            signed = w3.eth.account.sign_transaction(tx, PRIVATE_KEY)

            tx_hash = w3.eth.send_raw_transaction(signed.rawTransaction)

            with transaction.atomic():
                auction.ethereum_tx = tx_hash.hex()
                auction.save()
        except Exception as e:
            print(f"Error processing auction: {str(e)}")

