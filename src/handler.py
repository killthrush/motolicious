import pyfaaster.aws.handlers_decorators as faaster
import pyfaaster.aws.tools as tools

logger = tools.setup_logging('motolicious')


@faaster.http_response('Failed to process event.')
@faaster.namespace_aware
@faaster.body(required={'item1', 'item2'})
def process(event, context, NAMESPACE, body, **kwargs):

    response_body = body['item1']
    message_body = body['item2']

    return {
        'body': response_body,
        'messages': {
            'message-topic': {
                'message-payload': message_body,
            },
        },
    }
