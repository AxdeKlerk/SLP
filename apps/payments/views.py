from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings

def test_square(request):
    return HttpResponse(f"Square App ID: {settings.SQUARE_APPLICATION_ID}")
