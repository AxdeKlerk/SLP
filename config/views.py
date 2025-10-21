from django.shortcuts import render

print("DEBUG: Custom 404 handler called")


def error_404(request, exception):
    previous_page = request.META.get("HTTP_REFERER", "/")
    return render(request, "404.html", {"previous_page": previous_page}, status=404)


def error_500(request):
    previous_page = request.META.get("HTTP_REFERER", "/")
    return render(request, "500.html", {"previous_page": previous_page}, status=500)


# Testing 500 page
def crash_view(request):
    # This will crash on purpose
    1 / 0


#Testing 404 page
def test_404_template(request):
    return render(request, '404.html')