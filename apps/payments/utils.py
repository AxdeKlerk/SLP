import os
from square.client import Client

# Initialise Square client
client = Client(
    access_token=os.getenv("SQUARE_ACCESS_TOKEN"),
    environment="sandbox"  # or "production"
)
