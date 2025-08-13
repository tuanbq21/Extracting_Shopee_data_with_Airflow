import pytest
from unittest.mock import patch, MagicMock
import dags.shopee_client


@patch("dags.shopee_client.requests.get")
def test_fetch_ratings_success(mock_get):
    """Test khi API trả về thành công (status 200)."""
    # Giả lập response trả về thành công
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "ratings": [{"comment": "Hàng tốt", "rating_star": 5}]
    }
    mock_get.return_value = mock_response

    status_code, data = dags.shopee_client.shopee_client.fetch_ratings()

    mock_get.assert_called_once_with(dags.shopee_client.shopee_client.URL, headers=dags.shopee_client.shopee_client.HEADERS)
    assert status_code == 200
    assert "ratings" in data
    assert data["ratings"][0]["comment"] == "Hàng tốt"
    assert data["ratings"][0]["rating_star"] == 5


@patch("shopee_client.requests.get")
def test_fetch_ratings_fail(mock_get):
    """Test khi API trả về lỗi (status 404)."""
    mock_response = MagicMock()
    mock_response.status_code = 404
    mock_response.json.return_value = {"error": "Not Found"}
    mock_get.return_value = mock_response

    status_code, data = dags.shopee_client.shopee_client.fetch_ratings()

    assert status_code == 404
    assert "error" in data
    assert data["error"] == "Not Found"
