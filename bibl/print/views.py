from django.shortcuts import render, redirect
from textbook.models import TextBook, TextBookInvent


def single(request, isbn, inv):
    tb = TextBook.objects.filter(isbn=isbn)[0]
    data = {
        'isbn': isbn,
        'inv': inv.replace('.', '-'),
        'inv_print': inv,
        'textbook': tb,
        'media_root': media_root(request),
        'school': 'МАОУ СОШ 8',
    }
    return render(request, 'print/single.html', data)


def multi(request, isbn):
    tb = TextBook.objects.filter(isbn=isbn)[0]
    tbi = TextBookInvent.objects.filter(isbn=isbn)
    invm = []
    for i in tbi:
        spl = i.inv.split('.')
        inv = spl[0]
        nbook = spl[1]
        invm.append({'inv': inv, 'nbook': nbook})
    data = {
        'isbn': isbn,
        'textbook': tb,
        'invent': invm,
        'media_root': media_root(request),
        'school': 'МАОУ СОШ 8',
    }
    return render(request, 'print/multi.html', data)


def media_root(req):
    media_root = ''
    path = req.path
    a = len(path.split('/')) - 2
    for n in range(a):
        media_root += '../'
    media_root += 'media/'
    return media_root
