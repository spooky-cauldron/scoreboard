from http import HTTPStatus
from typing import Any


def not_found() -> tuple[dict[str, Any], int]:
    return {'error': 'not found'}, HTTPStatus.NOT_FOUND
