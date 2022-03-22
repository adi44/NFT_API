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
    txn_reciept = web3.eth.wait_for_transaction_receipt(txn_hash)
    if(txn_reciept['status']==1):
        data = contract.events.NFTContractCreated().processLog(txn_reciept['logs'][0])
        json_response = {}
        json_response['contract_id']= web3.toChecksumAddress(data['args']['nftcontract'])
        json_response['transaction_hash'] = str(web3.toHex(txn_hash))
        return json_response
    else:
        return "failed"

def mint_nft_token(contractAddress, walletAddress, metadata):
    all_deployed_tokens = all_nft_tokens()
    json_response = {}
    if(web3.toChecksumAddress(contractAddress) in all_deployed_tokens):
        contract = web3.eth.contract(address = web3.toChecksumAddress(contractAddress), abi = nft_abi)
        acct = web3.eth.account.privateKeyToAccount(private_key)
        tx = contract.functions.mintNFT(web3.toChecksumAddress(walletAddress), metadata).buildTransaction({
                   'from': acct._address,
                   'chainId':chainId,
                   'nonce': web3.eth.getTransactionCount(acct._address)})
        signed_tx = web3.eth.account.signTransaction(tx, private_key)
        txn_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
        txn_reciept = web3.eth.wait_for_transaction_receipt(txn_hash)
        if(txn_reciept['status']==1):
            json_response = {}
            json_response['transaction_hash'] = str(web3.toHex(txn_hash))
            return json_response
        else:
            json_response['status'] = 'failed'
            return json_response
    else:
        json_response['status'] = 'contract ID not deployed'
        return json_response

def all_nft_tokens():
     contract = web3.eth.contract(address = NFTFactoryContractAddress, abi = factory_abi)
     return contract.functions.getAlltokens().call()









