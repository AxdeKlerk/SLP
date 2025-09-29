import os
from square.client import Square, SquareEnvironment

# Initialise the Square client
# Uses your Heroku config var: SQUARE_ACCESS_TOKEN
# Environment should be "SANDBOX" while testing, "PRODUCTION" when live.
client = Square(
    access_token=os.getenv("SQUARE_ACCESS_TOKEN"),
    environment=SquareEnvironment.SANDBOX
)
