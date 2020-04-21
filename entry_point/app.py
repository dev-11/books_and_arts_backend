from datetime import datetime as dt
from services.service_factory import get_enabled_services
import json
import config as c


def lambda_handler(event, context):
    headers = event['params']['header']
    is_hard_get = parse_bool(headers[c.hard_load_header_key]) \
        if c.hard_load_header_key in headers \
        else False

    data = [{'family': service.get_service_family_name(),
             'service': service.get_service_name(),
             'full_name': service.get_service_full_name(),
             'data': service.get_data(is_hard_get)}
            for service in get_enabled_services()]

    return {
        'statusCode': 200,
        'body': {
            'fetched_at': json.dumps(f'{dt.now()}'),
            'data': data
        }
    }


def parse_bool(v):
    return str(v).lower() in ("yes", "true", "t", "1")
