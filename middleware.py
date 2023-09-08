import json
import logging
from functools import wraps

from flask import request
from pydantic import ValidationError

log = logging.getLogger()


def body(data_type: type):
    def body_decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                validated_body = data_type(**request.json)
                return func(validated_body, *args, **kwargs)
            except ValidationError as e:
                log.debug('Error validating data.')
                err_response = json.loads(e.json())
                for err in err_response:
                    if 'url' in err:
                        del err['url']
                log.debug(f'Validation Error: {err_response}')
                return err_response
        return wrapper
    return body_decorator
