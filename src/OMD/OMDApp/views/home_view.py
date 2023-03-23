from django.shortcuts import render

# Create your views here.
def LandingView(request):
    if request.user.is_authenticated:
        pass

    return render(request, 'land_page.html')