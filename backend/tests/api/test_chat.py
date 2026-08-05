"""Chat endpoint tests."""


def test_chat_returns_placeholder_response(client):
    response = client.post("/api/v1/chat", json={"message": "Plan a trip to Japan"})

    assert response.status_code == 200
    assert "response" in response.json()


def test_chat_rejects_empty_message(client):
    response = client.post("/api/v1/chat", json={"message": ""})

    assert response.status_code == 422
