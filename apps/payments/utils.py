import os
from square.client import client

# Initialise Square client
client = client.Client(
    access_token=os.getenv("SQUARE_ACCESS_TOKEN"),
    environment="sandbox"  # or "production"
)
