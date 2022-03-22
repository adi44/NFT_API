import boto3

dynamodb = boto3.resource('dynamodb')

table = dynamodb.create_table(
    TableName='apikeyholders',
    KeySchema = [
        {
            'AttributeName': 'ID',
            'KeyType': 'HASH'
        },
        {
            'AttributeName': 'API_KEY',
            'KeyType': 'RANGE'
        }
    ],
    AttributeDefinitions=[
        {
            'AttributeName': 'ID',
            'AttributeType': 'S'
        },
        {
            'AttributeName': 'API_KEY',
            'AttributeType': 'S'
        },
    ],
    ProvisionedThroughput={
        'ReadCapacityUnits': 100,
        'WriteCapacityUnits': 100
    }
)

table.wait_until_exists()
print(table.item_count)