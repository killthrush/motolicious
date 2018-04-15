import attrdict
import boto3
import moto
import os
import pytest
import simplejson as json

import src.handler as handler


@pytest.fixture(scope='function')
def context(mocker, lambda_context):
    context = attrdict.AttrMap()
    orig_env = os.environ.copy()
    os.environ['NAMESPACE'] = 'test'
    os.environ['CONFIG'] = 'config-bucket'
    context.os = {'environ': os.environ}
    context.mock_lambda_context = lambda_context
    yield context
    mocker.stopall()
    os.environ = orig_env


@moto.mock_sns
@moto.mock_sts
@pytest.mark.unit
@pytest.mark.api
def test_handler(context):
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
