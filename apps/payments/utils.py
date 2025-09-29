import os
from square.client import Client


client = Client(
    token=os.getenv("SQUARE_ACCESS_TOKEN"),
    environment='sandbox'  # change sandbox to "production" later
)
