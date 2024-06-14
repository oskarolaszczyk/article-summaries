from ..conftest import client


def test_server_connection(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json == {"message": "Server is up and running!"}
