"""Trip endpoint tests."""


def test_create_and_get_trip(client):
    create_response = client.post(
        "/api/v1/trips",
        json={
            "destination": "Japan",
            "start_date": "2026-10-01",
            "end_date": "2026-10-07",
        },
    )

    assert create_response.status_code == 201
    created = create_response.json()
    assert created["destination"] == "Japan"
    assert created["status"] == "planning"

    trip_id = created["id"]
    get_response = client.get(f"/api/v1/trips/{trip_id}")

    assert get_response.status_code == 200
    assert get_response.json()["destination"] == "Japan"


def test_get_missing_trip_returns_404(client):
    response = client.get("/api/v1/trips/00000000-0000-0000-0000-000000000000")

    assert response.status_code == 404


def test_create_trip_rejects_invalid_date_range(client):
    response = client.post(
        "/api/v1/trips",
        json={
            "destination": "Japan",
            "start_date": "2026-10-07",
            "end_date": "2026-10-01",
        },
    )

    assert response.status_code == 422
