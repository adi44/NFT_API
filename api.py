from hashlib import sha256
import uuid
from smartcontract import create_nft_token_contract, mint_nft_token
import flask
from flask import request
import boto3
from botocore.exceptions import ClientError
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('apikeyholders')
app = flask.Flask(__name__)

@app.route('/',methods=['GET'])
def greeting():
    return "Welcome to NFT Minting SDK : If you want to use it pls create API Key by going to /generateAPI_KEY"


@app.route('/generateAPI_KEY',methods=['GET'])
def generate_api_key():
    apiKey = str(uuid.uuid4())
    apiKeyHash = sha256(apiKey.encode()).hexdigest()
    table.put_item(
        Item={
            'ID' : str(apiKeyHash),
            'API_KEY':apiKey
        }
    )
    return ('Your API key is :' +apiKey)

@app.route('/nft/create',methods=['GET'])
def mint_nft_contract():
    api_key = str(request.args.get('api_key'))
    apiKeyHash = sha256(api_key.encode()).hexdigest()
    try:
        response = table.get_item(Key={'ID':str(apiKeyHash),'API_KEY':api_key})
        if response['Item']['API_KEY'] == api_key:
           return create_nft_token_contract()
    except ClientError as e:
        return e.response['Error']['Message']
    except KeyError:
        return 'API_KEY NOT FOUND'

@app.route('/nft/mint',methods=['GET'])
def mint_nft():
    api_key = str(request.args.get('api_key'))
    nft_contract_id = str(request.args.get('nft_contract_id'))
    wallet_address = str(request.args.get('wallet_address'))
    nft_metadata = str(request.args.get('nft_metadata'))

    apiKeyHash = sha256(api_key.encode()).hexdigest()

    try:
        response = table.get_item(Key={'ID':str(apiKeyHash),'API_KEY':api_key})
        if response['Item']['API_KEY'] == api_key:
            if(nft_contract_id and wallet_address and nft_metadata):
                return mint_nft_token(nft_contract_id,wallet_address,nft_metadata)
            else:
                return "Enter all the required parameters"
    except ClientError as e:
        return e.response['Error']['Message']
    except KeyError:
        return 'API_KEY NOT FOUND'

app.run()