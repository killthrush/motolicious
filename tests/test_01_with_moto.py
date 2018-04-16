import attrdict
import boto3
import moto
import os
import pytest

# Uncomment for sanity check
# import requests

import simplejson as json
import src.handler as handler


@pytest.fixture(scope='function')
def context(mocker, lambda_context):
    print('setup moto fixture')
    context = attrdict.AttrMap()

    # Uncomment for a sanity check - this should work if unpatching is working properly
    # requests.get('https://www.google.com')

    orig_env = os.environ.copy()
    os.environ['NAMESPACE'] = 'test'
    os.environ['CONFIG'] = 'config-bucket'
    context.os = {'environ': os.environ}
    context.mock_lambda_context = lambda_context

    # Uncomment to use patcher-style mocking
    # context.sts_mock = moto.mock_sts()
    # context.sns_mock = moto.mock_sns()
    # context.sts_mock.start()
    # context.sns_mock.start()

    yield context
    mocker.stopall()

    # Uncomment to use patcher-style mocking
    # context.sts_mock.stop()
    # context.sns_mock.stop()

    # Uncomment for a sanity check - this should work if unpatching is working properly
    # requests.get('https://www.google.com')

    os.environ = orig_env
    print('teardown moto fixture')


@moto.mock_sns
@moto.mock_sts
@pytest.mark.unit
@pytest.mark.api
def test_handler(context):
    print('start moto test')

    # Uncomment for a sanity check - this one should always fail if there's no passthrough
    # try:
    #
    #     requests.get('https://www.google.com')
    # except Exception:
    #     pass

    event = {
        'headers': {'origin': 'https://localhost'},
        'body': json.dumps({
            'item1': 'wassup?',
            'item2': 'foobar'
        })
    }
    boto3.client('sns').create_topic(Name=f'message-topic')
    response = handler.process(event, context.mock_lambda_context)
    assert response.get('statusCode') == 200
    body = json.loads(response.get('body'))
    assert body == 'wassup?'
    print('end moto test')
