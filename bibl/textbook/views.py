import os
import random

from django.shortcuts import render, redirect
from .models import TextBook, TextBookInvent, TextBookArhiv
from .forms import AddTextBookForm, AddTextBookInventForm, EditTextBookForm
import datetime
import qrcode
from django.views.generic import DetailView


def index(request):
    tb = TextBook.objects.order_by('isbn')
    tbtemp = []
    for i in range(len(tb)):
        otb = len(TextBookInvent.objects.filter(isbn=tb[i].isbn))
        tbtemp.append({
            'isbn': tb[i].isbn,
            'title': tb[i].title,
            'iteration': tb[i].iteration,
            'clas': tb[i].clas,
            'autor': tb[i].autor,
            'otb': otb
        })

    data = {
        'textbook': tbtemp,
        'local_nav': 'textbook/nav.html',
        'rnd': rnd()
    }

    return render(request, 'textbook/textbook.html', data)


def add(request):
    error = ''
    if request.method == 'POST':
        form = AddTextBookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('textbook')
        else:
            error = 'Форма неверная'

    form = AddTextBookForm()
    data = {
        'form': form,
        'error': error,
        'local_nav': 'textbook/nav.html',
        'now': nowdate(),
        'rnd': rnd()
    }
    return render(request, 'textbook/add.html', data)


def bookedit(request, isbn):
    error = ''
    tb = TextBook.objects.get(isbn=isbn)
    if request.method == 'POST':
        form = EditTextBookForm(request.POST)
        if form.is_valid():
            tb.title = str(request.POST.get('title'))
            tb.autor = str(request.POST.get('autor'))
            tb.year = str(request.POST.get('year'))
            tb.clas = str(request.POST.get('clas'))
            tb.publisher = str(request.POST.get('publisher'))
            tb.save()
            return redirect('textbook')
        else:
            error = 'Форма неверная '

    form = EditTextBookForm()

    data = {
        'form': form,
        'error': error,
        'local_nav': 'textbook/nav.html',
        'isbn': isbn,
        'tb': tb,
        'now': nowdate(),
        'rnd': rnd()
    }
    return render(request, 'textbook/edit.html', data)


def invent(request):
    tb = TextBook.objects.order_by('clas', 'title')
    tbtemp = []
    for i in range(len(tb)):
        otb = len(TextBookInvent.objects.filter(isbn=tb[i].isbn))
        tbtemp.append({
            'isbn': tb[i].isbn,
            'title': tb[i].title,
            'publisher': tb[i].publisher,
            'iteration': tb[i].iteration,
            'clas': tb[i].clas,
            'autor': tb[i].autor,
            'otb': otb
        })

    data = {
        'textbook': tbtemp,
        'local_nav': 'textbook/nav.html',
        'rnd': rnd()
    }

    return render(request, 'textbook/invent.html', data)


def TextBookDV(request, isbn):
    error = ''
    if request.method == 'POST':
        form = AddTextBookInventForm(request.POST)
        qol = int(request.POST.get('qol'))
        inv = str(request.POST.get('inv'))
        if form.is_valid():
            data = form.cleaned_data
            try:
                temp = TextBookInvent.objects.filter(isbn=isbn, inv__contains=inv).order_by('inv')
                if (len(temp)):
                    qol_first = int(temp[len(temp) - 1].inv.split('.')[1])
                else:
                    qol_first = 0
            except TextBookInvent.DoesNotExist:
                qol_first = 0
            qol = qol + qol_first
            for n in range(qol_first, qol):
                strn = str((n + 1))
                for q in range((3 - len(strn))):
                    strn = '0' + strn
                inv = data['inv'] + '.' + strn
                texbookinvent = TextBookInvent(inv=inv, isbn=isbn, date=data['date'])
                texbookinvent.save()

                qr = qrcode.QRCode(
                    version=1,
                    error_correction=qrcode.constants.ERROR_CORRECT_L,
                    box_size=10,
                    border=1,
                )
                qr_data = '888.' + inv
                qr.add_data(qr_data.replace('.', '-'))
                qr.make(fit=True)

                img = qr.make_image(fill_color="black", back_color="white")

                mediadir = os.path.join(os.getcwd(), 'bibl', 'media')
                if not os.path.isdir(mediadir):
                    os.mkdir(mediadir)
                qrdir = os.path.join(os.getcwd(), 'bibl', 'media', 'qrcode')
                if not os.path.isdir(qrdir):
                    os.mkdir(qrdir)

                path = os.path.join(os.getcwd(), 'bibl', 'media', 'qrcode', str(isbn))
                if not os.path.isdir(path):
                    os.mkdir(path)
                filename = os.path.join(path, inv.replace('.', '-') + ".png")
                img.save(filename)

            return redirect('/textbook/' + str(isbn))
        else:
            error = 'Форма неверная'

    tb = TextBook.objects.get(isbn=isbn)
    try:
        tbi = TextBookInvent.objects.filter(isbn=isbn)


    except TextBookInvent.DoesNotExist:
        tbi = ''

    if tbi:
        inventnumber = tbi[0].inv.split('.')[0]
    else:
        inventnumber = '0'

    allinventbook = len(tbi)

    form = AddTextBookInventForm
    data = {
        'textbook': tb,
        'textbookinvent': tbi,
        'inventnumber': inventnumber,
        'form': form,
        'now': nowdate(),
        'isbn': isbn,
        'local_nav': 'textbook/nav.html',
        'errot': error,
        'allinventbook': allinventbook,
        'rnd': rnd()
    }

    return render(request, 'textbook/textbookdv.html', data)


def delbook(request, invent):
    if int(invent.split('.')[0]) > 0:
        tbi = TextBookInvent.objects.get(inv=invent)
        isbn = tbi.isbn
        tbi.delete()
    else:
        ids = invent.replace ('-', '').split('.')
        for i in ids:
            tbi = TextBookInvent.objects.get(id=i)
            isbn = tbi.isbn
            tbi.delete()

    return redirect('/textbook/' + str(isbn))




def arhivbook(request, invent):
    if int(invent.split('.')[0]) > 0:
        tbi = TextBookInvent.objects.get(inv=invent)

        isbn = tbi.isbn
        inv = tbi.inv
        date = tbi.date

        tba = TextBookArhiv(inv=inv, isbn=isbn, date=date)
        tba.save()
        tbi.delete()

    else:
        ids = invent.replace('-', '').split('.')
        for i in ids:
            tbi = TextBookInvent.objects.get(id=i)
            isbn = tbi.isbn

            isbn = tbi.isbn
            inv = tbi.inv
            date = tbi.date

            tba = TextBookArhiv(inv=inv, isbn=isbn, date=date)
            tba.save()
            tbi.delete()


    return redirect('/textbook/' + str(isbn))




def nowdate():
    return datetime.datetime.today().strftime("%d.%m.%Y")


def rnd():
    return (random.random() * 10000) // 1
