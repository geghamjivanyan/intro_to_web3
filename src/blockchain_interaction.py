#
from typing import Optional

#
from web3 import Web3

#
from config import Config

#
class BlockchainInteraction:
    """
     BlockchainInteraction object for connect and interact with smart contract
    """

    #
    def __init__(self, config: Optional[Config]) -> None :
        """
         Constructor

         :param config: Config object contains all necessary credentials
         
         :returns: None
        """
        self.config = config
        self.is_connected = False
        self.w3 = None
        self.contract = None

    #
    def __is_connected(self) -> None:
        """
        Connect to blockchain

        :returns: connection state
        """
        w3 = Web3(Web3.HTTPProvider('{}/{}'.format(self.config.BLOCKCHAIN_URL, self.config.project_id)))
        if w3.isConnected():
            self.is_connected = True
            self.w3 = w3
            return True
        return False

    def __generate_private_key(self, length: int) -> str:
        """
         Generate 64-byte private key

         :param length: length of private key 

         :returns: None
        """

        #
        import string
        import random


        alphabet62 = string.digits + string.ascii_letters

        self.config.private_key = '0x' + ''.join(random.choice(alphabet62) for _ in range(length))



    #
    def __generate_account(self) -> None:
        """
        Generate account for interaction

        :returns: None
        """
        acnt = self.config.w3.eth.account.privateKeyToAccount(self.config.private_key)
        self.config.account_address = acnt.address



    #
    def __setup_contract(self) -> None:
        """
        setup contract and account if connected

        :returns: None
        """
        if self.is_connected:
            self.__generate_private_key(self, 64)
            self.__generate_account()
            self.w3.eth.defaultAccount = self.config.account_address
            self.contract = self.w3.eth.contract(address=self.config.contract_address, abi = self.config.abi)

    #
    def setup(self) -> None:
        """
         setup connection and contract

         :returns: None
        """
        self.__is_connected()
        if self.is_connected:
            self.__setup_contract()
    #
    def all_functions(self) -> list:
        """
         List of all smart contract functions

         :returns: list of function descriptions
        """
        return self.contract.all_functions()

    #
    def write_to_blockchain(self, data) -> bool:
        """
        Write data to blockchain

        :param data: any kind of data due to smart contract function which will be called

        :returns: transaction successfull state

        """
        if self.is_connected:
            est_gas = self.contract.functions.insertDigest(
                    '0x' + data['hash'], 
                    data['meta'], 
                    data['owner'], 
                    data['user_id']).estimateGas()
            
            transaction = self.contract.functions.insertDigest(
                    '0x' + data['hash'], 
                    data['meta'], 
                    data['owner'], 
                    data['user_id']).buildTransaction({
                            'gas': est_gas + 10000, 
                            'gasPrice': Web3.toWei('1', 'gwei'), 
                            'from': self.config.account_address, 
                            'nonce': self.w3.eth.getTransactionCount(self.config.account_address)
                        })
            
            signed_txn = self.w3.eth.account.signTransaction(
                    transaction, 
                    private_key=self.config.private_key)
            
            output = self.w3.eth.sendRawTransaction(signed_txn.rawTransaction)
            
            txn_receipt = self.w3.eth.waitForTransactionReceipt(output)
        return True


    def get_from_blockchain(self, data):
        """ 
         Read data from blockchain

         :param data: any kind of data due to smart contract function which will be called

         :returns: data read from blockchain
        """
        if self.is_connected:
            return self.contract.functions.getDigest('0x' + data).call()


    def __repr__(self) -> None:
        """
         Representaion of BlockchainInteraction object

         :returns: Stringified BlockchainInteraction object
        """
        return "IS CONNECTED - {}\nW3 - {}\nCONTRACT - {}\n".format(self.is_connected, self.w3, self.contract)
