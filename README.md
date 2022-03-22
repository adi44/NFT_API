# NFT_API

This API can be used to mint a nft from any specific NFT contract deployed using our API. There are total two endpoints. 
Endpoint 1 : /nft/create
This endpoing to create NFT from the NFT contract Deployed on Mumbai Testnet.

Endpoint 2 : /nft/mint
This is the endpoint to mint NFT from any contract that created using endpoint 1

## How to set up the Dev Environment (for devs)

Ensure that you have Python3.x and pip3 installed on your device.

### You need to setup the env File

Following are the parameters that you need to add

  PRIVATE_KEY= \
  INFURA_URL= \
  NFT_FACTORY_ADDRESS= \
  CHAIN_ID= \

From Step 1 to Step 5 : you would be able to set up the dynamoDB web service which will be used to store all the generated API keys.

Step 1 : Create a aws account, and generate a access key and access key secret \
Step 2 : install aws cli \
Step 3 : configure user using access key and access key secret \
Step 4 : install Boto3 aws Sdk for python \
Step 5 : run ```python3 db.py``` \
Step 6 : run ```python3 api.py``` \
This will start the server and you can use the endpoints. \

## How to use the API {for users}

Step 1 : generate the API Key by going to the  `./generateAPIKey` endpoint \
Step 2 : to mint NFT contract go to  `./mft/create?api_key=API_KEY_GENERATED` enpoint \
Step 3 : to mint NFT token goto `./nft/create?api_key=API_KEY_GENERATED&nft_contract_id=NFT_CONTRACT_ADDRESS&wallet_address=WALLET_ADDRESS&nft_metadata=NFT_METADATA` \

Both of the endpoint will return a transaction hash that you can check on https://mumbai.polygonscan.com \

Users do not need to use any wallet to mint NFT or create Contract

