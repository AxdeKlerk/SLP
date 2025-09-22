from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from .utils import client

def test_square(request):
    return HttpResponse(f"Square App ID: {settings.SQUARE_APPLICATION_ID}")

def test_square_connection(request):
    result = client.locations.list()
    
    if hasattr(result, "errors") and result.errors:
        return JsonResponse({"errors": [e.detail for e in result.errors]})

    # Convert locations (which will be a list of models) into dicts for JSON
    locations = [loc.dict() for loc in result.locations] if result.locations else []

    return JsonResponse({"locations": locations})
