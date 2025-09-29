import os
from square.client import Square, SquareEnvironment

# Initialise the Square client directly with token
square = Square(
    access_token=os.getenv("SQUARE_ACCESS_TOKEN"),
    environment=SquareEnvironment.SANDBOX  # change to PRODUCTION when live
)

# Example: expose the payments API
payments_api = square.payments
