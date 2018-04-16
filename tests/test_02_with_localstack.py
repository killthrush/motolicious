import attrdict
import pytest

# Uncomment for sanity check
# import requests

import src.dynamo_facade as facade
import tests.dynamodb_helpers as dh


_TEST_RECORDS = [
    {'key': 'foo',
     'value': 'foobar'},
    {'key': 'bar',
     'value': 'barbar'},
    {'key': 'baz',
     'value': 'bazbar'},
]


@pytest.fixture(scope='function')
def test_table(dynamodb):
    # Uncomment for a sanity check - this should work if unpatching is working properly
    # requests.get('https://www.google.com')

    table = dh.create_table(dynamodb,
                            'test-dynamo',
                            keys=[('key', 'HASH', 'S')])
    yield table

    # Uncomment for a sanity check - this should work if unpatching is working properly
    # requests.get('https://www.google.com')
    table.delete()


@pytest.fixture(scope='function')
def table_with_records(test_table):
    for item in _TEST_RECORDS:
        test_table.put_item(Item=item)
    yield test_table


@pytest.fixture(scope='function')
def context(table_with_records):
    context = attrdict.AttrMap()
    context.table = table_with_records
    yield context


@pytest.mark.integration
@pytest.mark.dynamodb
def test_set_value(context):
    print('start localstack test')

    # Uncomment for a sanity check - this should work if unpatching is working properly
    # requests.get('https://www.google.com')

    output = facade.set_value(context.table, 'foo', 'monkey')
    assert output is not None

    # Uncomment for a sanity check - this should work if unpatching is working properly
    # requests.get('https://www.google.com')

    print('end localstack test')
