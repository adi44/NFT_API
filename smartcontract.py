from itertools import chain
from web3 import Web3
from web3.middleware import geth_poa_middleware
from decouple import config
import json
f = open('erc721ADFactory.json')
factory_abi = json.load(f)
f_new = open('erc721AD.json')
nft_abi = json.load(f_new)
infura_url = config('INFURA_URL')
web3 = Web3(Web3.HTTPProvider(infura_url))
web3.middleware_onion.inject(geth_poa_middleware, layer=0)
private_key = config('PRIVATE_KEY')
print(web3.isConnected())

NFTFactoryContractAddress = config('NFT_FACTORY_ADDRESS')
chainId = int(config('CHAIN_ID'))


def create_nft_token_contract():
    contract = web3.eth.contract(address = NFTFactoryContractAddress, abi = factory_abi)
    acct = web3.eth.account.privateKeyToAccount(private_key)
    tx = contract.functions.createERC721AD().buildTransaction({
                   'from': acct._address,
                   'chainId':chainId,
                   'nonce': web3.eth.getTransactionCount(acct._address)})
    signed_tx = web3.eth.account.signTransaction(tx, private_key)
    txn_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
    json_response = {}
    json_response['transaction_hash'] = str(web3.toHex(txn_hash))
    return json_response

def mint_nft_token(contractAddress, walletAddress, metadata):
    contract = web3.eth.contract(address = contractAddress, abi = nft_abi)
    acct = web3.eth.account.privateKeyToAccount(private_key)
    tx = contract.functions.mintNFT(walletAddress, metadata).buildTransaction({
                   'from': acct._address,
                   'chainId':chainId,
                   'nonce': web3.eth.getTransactionCount(acct._address)})
    signed_tx = web3.eth.account.signTransaction(tx, private_key)
    txn_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
    json_response = {}
    json_response['transaction_hash'] = str(web3.toHex(txn_hash))
    return json_response





