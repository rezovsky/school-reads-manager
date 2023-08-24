import hashlib
import os

import qrcode
from django.shortcuts import render, redirect
from textbook.models import TextBook, TextBookInvent


def single(request, isbn, inv):
    url = qr_generate(isbn, inv)
    tb = TextBook.objects.filter(isbn=isbn)[0]
    data = {
        'isbn': isbn,
        'inv': inv.replace('.', '-'),
        'inv_print': inv,
        'textbook': tb,
        'media_root': media_root(request),
        'school': 'МАОУ СОШ 8',
        'url': url
    }
    return render(request, 'print/single.html', data)


def multi(request, isbn):
    tb = TextBook.objects.filter(isbn=isbn)[0]
    tbi = TextBookInvent.objects.filter(isbn=isbn)
    invm = []
    for i in tbi:
        url = qr_generate(isbn, i.inv)
        spl = i.inv.split('.')
        inv = spl[0]
        nbook = spl[1]
        invm.append({'inv': inv, 'nbook': nbook, 'url': url})
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


def qr_generate(isbn, inv):
    media_path = os.path.join(os.getcwd(), 'media')
    if not os.path.isdir(media_path):
        os.mkdir(media_path)

    qrcode_path = os.path.join(media_path, 'qrcode')
    if not os.path.isdir(qrcode_path):
        os.mkdir(qrcode_path)

    isbn_hash = hashlib.md5(str(isbn).encode('utf-8')).hexdigest()
    path = os.path.join(qrcode_path, isbn_hash)
    if not os.path.isdir(path):
        os.mkdir(path)

    inv_hash = hashlib.md5(inv.encode('utf-8')).hexdigest()
    file_path = os.path.join(path, f"{inv_hash}.png")

    if not os.path.exists(file_path):
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
        img.save(file_path)

    return f"qrcode/{isbn_hash}/{inv_hash}.png"
