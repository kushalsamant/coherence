"""
Test helper functions for backend tests
"""
from typing import Dict, Any
import json


def create_razorpay_webhook_payload(
    event: str,
    payload_data: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Create a mock Razorpay webhook payload
    
    Args:
        event: Webhook event name (e.g., "payment.captured")
        payload_data: Event-specific payload data
    
    Returns:
        Complete webhook payload dict
    """
    base_payload = {
        "entity": "event",
        "account_id": "acc_test123",
        "event": event,
        "contains": [],
        "payload": {
            "payment": {},
            "subscription": {},
        },
        "created_at": 1640995200,
    }
    
    # Merge payload data
    if "payment" in payload_data:
        base_payload["payload"]["payment"].update(payload_data["payment"])
    
    if "subscription" in payload_data:
        base_payload["payload"]["subscription"].update(payload_data["subscription"])
    
    # Update contains based on payload
    if base_payload["payload"]["payment"]:
        base_payload["contains"].append("payment")
    if base_payload["payload"]["subscription"]:
        base_payload["contains"].append("subscription")
    
    return base_payload


def create_mock_razorpay_checkout_response(
    order_id: str = "order_test123",
    amount: int = 129900,
    currency: str = "INR"
) -> Dict[str, Any]:
    """
    Create a mock Razorpay checkout response
    
    Args:
        order_id: Razorpay order ID
        amount: Amount in paise
        currency: Currency code
    
    Returns:
        Mock checkout response dict
    """
    return {
        "success": True,
        "data": {
            "key_id": "rzp_test_xxxxx",
            "order_id": order_id,
            "amount": amount,
            "currency": currency,
            "name": "Test Product",
            "description": "Test Description",
            "prefill": {
                "email": "test@example.com",
            },
            "notes": {
                "app": "test",
            },
        }
    }


def create_mock_razorpay_subscription_response(
    subscription_id: str = "sub_test123",
    plan_id: str = "plan_test123",
    status: str = "active"
) -> Dict[str, Any]:
    """
    Create a mock Razorpay subscription response
    
    Args:
        subscription_id: Subscription ID
        plan_id: Plan ID
        status: Subscription status
    
    Returns:
        Mock subscription response dict
    """
    return {
        "id": subscription_id,
        "entity": "subscription",
        "plan_id": plan_id,
        "status": status,
        "current_start": 1640995200,
        "current_end": 1643587200,
        "end_at": None,
        "quantity": 1,
        "notes": {},
        "charge_at": 1643587200,
        "created_at": 1640995200,
    }


def assert_success_response(response, expected_data: Dict[str, Any] = None):
    """
    Assert that a response is a successful API response
    
    Args:
        response: FastAPI test client response
        expected_data: Optional expected data to verify
    """
    assert response.status_code == 200
    data = response.json()
    assert data.get("success") is True
    
    if expected_data:
        assert "data" in data
        for key, value in expected_data.items():
            assert data["data"].get(key) == value


def assert_error_response(response, expected_status: int = 400, expected_code: str = None):
    """
    Assert that a response is an error API response
    
    Args:
        response: FastAPI test client response
        expected_status: Expected HTTP status code
        expected_code: Optional expected error code
    """
    assert response.status_code == expected_status
    data = response.json()
    assert data.get("success") is False
    assert "error" in data
    
    if expected_code:
        assert data["error"].get("code") == expected_code

