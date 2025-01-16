import ujson

from requests import Response


class MockClientResponse:
    status: int
    content: bytes

    def __init__(self, content, status):
        self.content = ujson.dumps(content).encode()
        self.status = status

    async def read(self):
        return self.content


class MockRequests:
    status: int
    content: bytes

    def __init__(self, monkeypatch, response_body: dict, response_status: int):
        self.content = ujson.dumps(response_body).encode()
        self.status = response_status
        monkeypatch.setattr("requests.Session.request", self.mock_request)

    def mock_request(self, *args, **kwargs):
        response = Response()
        response.status_code = self.status
        response._content = self.content
        return response
