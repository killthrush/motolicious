def build_table_def(table_name, keys, additional_attributes=None, global_secondary_indices=None):
    """
    Creates a minimal dynamodb definition suitable for use with localstack.

    Args:
        table_name: The full name of the test table
        keys: The key definitions to use - a list of 4-tuples (<name>, <key_type>, <data_type>, <index_name>).
              For example - ('cz_res_id', 'HASH', 'S', 'MyGSI')
        additional_attributes: additional attributes, beyond the keys, that need to be defined
        global_secondary_indices: The list of keys for which global secondary indices will be
        generated. global_secondary_indices must be a subset of 'keys'.

    Returns:
        A dict containing the table def - suitable for use with boto3.
    """
    all_attributes = [{'AttributeName': k[0], 'AttributeType': k[2]} for k in keys]
    all_attributes = all_attributes + [{'AttributeName': a[0], 'AttributeType': a[1]}
                                       for a in (additional_attributes or [])]
    table_def = {
        'TableName': table_name,
        'KeySchema': [{'AttributeName': k[0], 'KeyType': k[1]} for k in keys],
        'AttributeDefinitions': all_attributes,
        'ProvisionedThroughput': {
            'ReadCapacityUnits': 1,
            'WriteCapacityUnits': 1
        }
    }
    if global_secondary_indices:
        table_def['AttributeDefinitions'] += [
            {
                'AttributeName': k[0],
                'AttributeType': k[2]
            } for k in global_secondary_indices
        ]
        table_def['GlobalSecondaryIndexes'] = [
            {
                'IndexName': f'{k[3]}',
                'ProvisionedThroughput': table_def['ProvisionedThroughput'],
                'KeySchema': [
                    {
                        'AttributeName': k[0],
                        'KeyType': k[1],
                    }
                ],
                'Projection': {'ProjectionType': 'ALL'}
            }
            for k in global_secondary_indices
        ]
    return table_def


def create_table(dynamodb, table_name, keys, additional_attributes=None, global_secondary_indices=None):
    table_definition = build_table_def(table_name, keys, additional_attributes=None,
                                       global_secondary_indices=global_secondary_indices)
    table = dynamodb.create_table(**table_definition)
    table.meta.client.get_waiter('table_exists').wait(TableName=table_name)
    return table
