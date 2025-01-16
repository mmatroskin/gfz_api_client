from datetime import datetime, timezone

from gfz_client import settings
from gfz_client.exceptions import InternalServiceError


def from_date_string(date_str: str) -> datetime:
    try:
        result = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
    except ValueError:
        raise InternalServiceError("Malformed date parameter on input")
    else:
        if not result.tzinfo:
            result = result.replace(tzinfo=timezone.utc)
        return result


def to_date_string(date: datetime) -> str:
    return date.strftime('%Y-%m-%dT%H:%M:%SZ')


def check_date(start_time: datetime, end_time: datetime):
    if start_time > end_time:
        raise InternalServiceError("Start time must be before or equal to end time")


def check_index_name(index: str):
    if index not in settings.INDEX_LIST:
        raise InternalServiceError("Malformed parameter on input: index")


def check_status(status: str):
    if status not in settings.STATE_LIST:
        raise InternalServiceError("Malformed parameter on input: status")
