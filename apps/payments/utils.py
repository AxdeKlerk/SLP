import os
from square.client import Square, SquareEnvironment

client = Square(
    token=os.getenv("SQUARE_ACCESS_TOKEN"),
    environment=SquareEnvironment.SANDBOX # change sandbox to "production" later
)
