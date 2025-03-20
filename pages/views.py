from django.shortcuts import render
from django.http import HttpResponse
# from services.models import Service

def index(request):
    # services = Service.objects.all().filter(is_published=True)[:3]

    # context = {
    #     'services': services
    # }
    return render(request, 'pages/index.html')

def about(request):
    return render(request, 'pages/about.html')

# def custom_404_view(request, exception):
#     return render(request, '404.html', {'path': request.path}, status=404)

# def test_500(request):
#     raise Exception("Simulated server error for testing 500 page")