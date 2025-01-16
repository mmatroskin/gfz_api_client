from unittest.mock import patch
import pytest

from gfz_client import GFZClient, GFZAsyncClient
from tests.utils import MockRequests, MockClientResponse

test_data = (
    (
        ("2011-11-04T00:05:23Z", "2011-11-04T00:05:24", "Kp", "def"),
        ({"Kp": [10], "datetime": [], "status": ["test"]}, 200),
        {
            "get_kp_index": ((), (10,), ('test',)),
            "get_nowcast": {
                "Kp": [10],
                "datetime": [],
                "status": ["test"]
            },
            "get_forecast": {
                "Kp": [10],
                "datetime": [],
                "status": ["test"]
            }
        }
    ),
    (
        ("2011-11-04T00:05:23Z", "2011-11-04T00:05:24", "Kp", "def"),
        (None, 400),
        {
            "get_kp_index": (0, 0, 0),
            "get_nowcast": "Remote service response status: 400",
            "get_forecast": "Remote service response status: 400"
        }
    ),
    (
        ("2011-11-04T00:05:23Z", "2011-11-04T00:05:22", "Kp", "def"),
        (None, 200),
        {
            "get_kp_index": (0, 0, 0),
            "get_nowcast": "Start time must be before or equal to end time",
            "get_forecast": "Invalid response"
        }
    ),
    (
        ("2011-11-04T00:05:23z", "2011-11-04T00:05:24", "Kp", "def"),
        (None, 200),
        {
            "get_kp_index": (0, 0, 0),
            "get_nowcast": "Malformed date parameter on input",
            "get_forecast": "Invalid response"
        }
    ),
    (
        ("2011-11-04T00:05:23Z", "2011-11-04T00:05:24", "Kp0", "def"),
        (None, None),
        {
            "get_kp_index": (0, 0, 0),
            "get_nowcast": "Malformed parameter on input: index",
            "get_forecast": "Malformed parameter on input"
        }
    ),
    (
        ("2011-11-04T00:05:23Z", "2011-11-04T00:05:24", "Fobs", "def"),
        (None, 200),
        {
            "get_kp_index": (0, 0, 0),
            "get_nowcast": "Invalid response",
            "get_forecast": "Malformed parameter on input"
        }
    ),
    (
        ("2011-11-04T00:05:23Z", "2011-11-04T00:05:24", "Kp", "test"),
        (None, 200),
        {
            "get_kp_index": (0, 0, 0),
            "get_nowcast": "Malformed parameter on input: status",
            "get_forecast": "Invalid response"
        }
    )
)


@pytest.mark.parametrize("data, response, expected", test_data)
def test_client(monkeypatch, data, response, expected):
    client = GFZClient()
    MockRequests(monkeypatch=monkeypatch, response_body=response[0], response_status=response[1])
    try:
        result = client.get_kp_index(data[0], data[1], data[2], status=data[3])
    except Exception as exc:
        result = exc
    assert result == expected["get_kp_index"]
    try:
        result = client.get_nowcast(data[0], data[1], data[2], data_state=data[3])
    except Exception as exc:
        result = str(exc)
    assert result == expected["get_nowcast"]
    try:
        result = client.get_forecast(data[2])
    except Exception as exc:
        result = str(exc)
    assert result == expected["get_forecast"]


@patch("aiohttp.client.ClientSession.request")
@pytest.mark.parametrize("data, response, expected", test_data)
@pytest.mark.asyncio
async def test_async_client(mock_engine, data, response, expected):
    mock_engine.return_value.__aenter__.return_value = MockClientResponse(content=response[0], status=response[1])
    client = GFZAsyncClient()
    try:
        result = await client.get_kp_index(data[0], data[1], data[2], status=data[3])
    except Exception as exc:
        result = exc
    assert result == expected["get_kp_index"]
    try:
        result = await client.get_nowcast(data[0], data[1], data[2], data_state=data[3])
    except Exception as exc:
        result = str(exc)
    assert result == expected["get_nowcast"]
    try:
        result = await client.get_forecast(data[2])
    except Exception as exc:
        result = str(exc)
    assert result == expected["get_forecast"]
