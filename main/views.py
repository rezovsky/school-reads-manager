from django.shortcuts import render


def index(request):
    return render(request, 'main/index.html')


def main(request):
    return render(request, 'main/main.html')
