import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_stream_video():
    response = client.get("/stream")
    print(response.headers)
    assert response.status_code == 200
    stream_content_type = ' '.join(response.headers["content-type"].split())
    assert stream_content_type == "multipart/x-mixed-replace; boundary=frame"


if __name__ == "__main__":
    pytest.main()
