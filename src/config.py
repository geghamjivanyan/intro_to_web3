import ast
# Class contain config params

class Config:
    """
    Config object contains all credentials for connecting to blockchain smart contract
    """

    # ropsten api url prefix
    BLOCKCHAIN_URL = 'https://ropsten.infura.io/v3'
    
    # 
    def __init__(self, pr_id: str, abi: list, cont_addr: str) -> None:
        """
         Constructor 
         :param project_id: Infura project id
         :param abi: smart contract abi
         :param cont_addr: smart contract address

         :returns: None
         
        """
        self.project_id = pr_id
        self.account_address = None
        self.abi = ast.literal_eval(str(abi))
        self.contract_address = cont_addr
        self.private_key = None



