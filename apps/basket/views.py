from django.shortcuts import render

def basket_view(request):
    return render(request, 'basket/basket.html')
