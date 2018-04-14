import os
import boto3
import pyfaaster.aws.tools as tools

logger = tools.setup_logging('motolicious')


def table(namespace):
    name = f'motolicious-{namespace}-test-table'
    dynamodb_endpointurl = os.environ.get('DYNAMODB_ENDPOINTURL')
    if dynamodb_endpointurl:
        logger.debug(f'Connecting to {name} table at {dynamodb_endpointurl}')
        return boto3.resource('dynamodb', endpoint_url=dynamodb_endpointurl).Table(name)
    else:
        logger.debug(f'Connecting to {name} table using default endpoint')
        return boto3.resource('dynamodb').Table(name)


def set_value(table, key, value):
    logger.debug(f'Saving {value} for {key} in {table.name}')

    try:
        policy = table.update_item(
            Key={'key': key},
            UpdateExpression=f'SET #name = :type_value',
            ExpressionAttributeNames={
                '#name': 'value'
            },
            ExpressionAttributeValues={
                ':type_value': value
            },
            ReturnValues='ALL_NEW'
        )
        logger.debug(f'Saved record to {table.name}')
        return policy
    except Exception as err:
        logger.exception(err)
        raise Exception('General boto error')
