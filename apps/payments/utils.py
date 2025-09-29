import os
from square.client import Square, SquareEnvironment

# Create the Square client WITHOUT token
square = Square(
    environment=SquareEnvironment.SANDBOX  # change to PRODUCTION when live
)

# Attach the token afterwards
square.access_token = os.getenv("SQUARE_ACCESS_TOKEN")

# Expose the payments API
payments_api = square.payments

# Expose other APIs similarly, e.g., customers_api = square.customers