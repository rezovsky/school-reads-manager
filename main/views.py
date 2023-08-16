from django.shortcuts import render

def index(request):
    data = {
        'local_nav': 'main/nav.html'
    }
    return render(request, 'main/index.html', data)