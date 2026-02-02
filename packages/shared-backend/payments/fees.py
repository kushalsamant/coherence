"""
Payment processing fee utilities
"""

# Razorpay fee percentage (2%)
RAZORPAY_FEE_PERCENTAGE = 0.02


def calculate_processing_fee(amount: int) -> int:
    """
    Calculate Razorpay processing fee (2% of amount).
    
    Args:
        amount: Payment amount in paise (₹1 = 100 paise)
        
    Returns:
        Processing fee in paise
    """
    return int(amount * RAZORPAY_FEE_PERCENTAGE)

