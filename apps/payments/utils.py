import os
from square.client import Square, SquareEnvironment

# Initialise Square client
client = Square(
    access_token=os.getenv("SQUARE_ACCESS_TOKEN"),
    environment=SquareEnvironment.SANDBOX  # or SquareEnvironment.PRODUCTION
)
