from django.shortcuts import render


menu = [
    {'title':"About site",
     'url_name': 'about'},
     ]

# Create your views here.
def profile(request):
    context = {
        'title': "Your profile",
        'menu': menu,
    }
    return render(request, 'chat/profile.html', context)
