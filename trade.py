from web3 import Web3
import solcx

class NFT_trading():
    def __init__(self, network, buy_address, sell_address):
        self.w3 = Web3(Web3.HTTPProvider(network))
        self.buy_address = buy_address
        self.sell_address = sell_address
        self.__compile("ERC721.sol")
        self.__deploy()
    def __compile(self, source_file_path, compiler_version="0.8.7"):
        solcx.set_solc_version(compiler_version) # set compiler version
        with open(source_file_path, 'r') as f:
            source = f.read()
        compiled_sol = solcx.compile_source(source=source, allow_paths = ['/Users/gunu/Documents/team12/nft/'], output_values=['abi', 'bin'])  # path allowance should be done for security reason
        contract_id, contract_interface = compiled_sol.popitem() 
        self.abi=contract_interface['abi'] # get abi, bin
        self.bytecode=contract_interface['bin']

    def __eth_transfer(self, eth_value): # price unit will be ETH not Wei
        tx_hash = self.w3.eth.send_transaction({
        'to': self.sell_address,
        'value': self.w3.toWei(eth_value, 'ether'),
        'from': self.buy_address,
        'gas': 21000,
        'maxFeePerGas': self.w3.toWei(250, 'gwei'),
        'maxPriorityFeePerGas': self.w3.toWei(2, 'gwei'),
        })
        return tx_hash

    def __deploy(self):
        ###CONTRACT DEPLOY PART###
        self.w3.eth.default_account = self.buy_address # set default account for minting
        contract_tx_hash = self.w3.eth.contract(abi=self.abi, bytecode=self.bytecode).constructor().transact() # deploy mint contract
        contract_address = self.w3.eth.get_transaction_receipt(contract_tx_hash)['contractAddress']
        self.mint_contract = self.w3.eth.contract(address = contract_address, abi=self.abi)

    def buy_nft(self, URI, price):
        ###MINT & TRASNFER PART###
        eth_transfer_tx_hash = self.__eth_transfer(price) # transfer eth to seller_account
        mint_tx_hash = self.mint_contract.functions.mintNFT(self.buy_address, URI).transact() # mint token to buyer_account
        return mint_tx_hash, eth_transfer_tx_hash