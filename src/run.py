from hashlib import sha256

from blockchain_interaction import BlockchainInteraction
from config import Config

PROJECT_ID = 'YOUR_PROJECT_ID'
ACCOUNT_ADDRESS = 'YOUR_ACCOUNT_ADDRESS'
CONTRACT_ADDRESS = 'YOUR_SMART_CONTRACT_ADDRESS'
PRIVATE_KEY = 'YOUR_PRIVATE_KEY'

ABI = 'YOUR_SMART_CONTRACT_ABI' 


def hash_info(info):
    return sha256(str(info).encode()).hexdigest()


if __name__ == "__main__":
    cfg = Config(PROJECT_ID, ACCOUNT_ADDRESS, ABI, CONTRACT_ADDRESS, PRIVATE_KEY)
    bi = BlockchainInteraction(cfg)
    bi.setup()

    print("OBJECT - ", bi)
    print("ALL FUNCTIONS - ", bi.all_functions())

    data = {'hash': hash_info("bla-bla-bla"), 'owner': 'PYerevan', 'user_id': 1, 'meta': ''}
    
    bi.write_to_blockchain(data)

    print(bi.get_from_blockchain(hash_info('bla-bla-bla')))
