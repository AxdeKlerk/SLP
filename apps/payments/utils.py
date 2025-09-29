import os
from square.client import Square, SquareEnvironment

# Initialise the Square client
square = Square(
    environment=SquareEnvironment.SANDBOX  # change to PRODUCTION when live
)

# Attach the access token after initialisation
square.config.access_token = os.getenv("SQUARE_ACCESS_TOKEN")

# Example: expose the payments API so views can import it
payments_api = square.payments
