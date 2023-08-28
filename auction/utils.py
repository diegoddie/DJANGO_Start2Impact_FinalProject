from web3 import Web3, HTTPProvider
from dotenv import load_dotenv
import os
from web3 import Web3
load_dotenv()

def connect_to_ethereum():
    ethereum_url = os.environ.get('ETHEREUM_URL')
    
    try:
        w3 = Web3(Web3.HTTPProvider(ethereum_url))
        if w3.is_connected():
            return w3
        else:
            raise Exception("Failed to connect to Ethereum node")
    except Exception as e:
        print(f"Error connecting to Ethereum: {e}")
        return None
    