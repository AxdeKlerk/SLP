import os
from square.client import Square, SquareEnvironment

# Initialise Square client
client = Square(
    environment=SquareEnvironment.SANDBOX  # change to PRODUCTION when live
)

# Attach the token after init (if supported by this SDK)
token = os.getenv("SQUARE_ACCESS_TOKEN")
if token:
    client.access_token = token

# Example: expose the payments API
payments_api = client.payments

# Example: expose the orders API
orders_api = client.orders