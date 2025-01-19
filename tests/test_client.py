from unittest.mock import patch
import pytest

from gfz_client import GFZClient, GFZAsyncClient
from tests.utils import MockRequests, MockClientResponse, get_test_data


test_data = get_test_data()


@pytest.mark.parametrize("data, response, expected", test_data)
def test_client(monkeypatch, data, response, expected):
    client = GFZClient()
    MockRequests(monkeypatch=monkeypatch, response_body=response[0], response_status=response[1])
    result = client.get_kp_index(data[0], data[1], data[2], status=data[3])
    assert result == tuple(tuple(item) if isinstance(item, list) else item for item in expected["get_kp_index"])
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
    result = await client.get_kp_index(data[0], data[1], data[2], status=data[3])
    assert result == tuple(tuple(item) if isinstance(item, list) else item for item in expected["get_kp_index"])
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
