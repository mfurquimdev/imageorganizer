from django.shortcuts import render, redirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage

from uploads.core.models import Document, Sprite
from uploads.core.forms import DocumentForm, SpriteForm

from uploads.core.load import load_all_images

import numpy as np
from scipy import linalg, optimize

from django.core.files.storage import default_storage

import sys
import os
import subprocess as sub

def home(request):
    sprites = Sprite.objects.all()
    return render(request, 'core/home.html', { 'sprites': sprites[:10] })

def organize(request):
    sprites = Sprite.objects.all()
    return render(request, 'organize/organize.html', { 'sprites': sprites[:10] })

def clean(request):
    Sprite.objects.all().delete()
    sprites = Sprite.objects.all()
    p = sub.Popen(['/usr/bin/rm', '-rf', '/home/mfurquim/projects/imageorganizer/media/sprites/'],stdout=sub.PIPE,stderr=sub.PIPE)
    return render(request, 'core/home.html', { 'sprites': sprites })

def load_all(request):
    images = load_all_images()
    sprites = Sprite.objects.all()
    return render(request, 'core/home.html', { 'sprites': sprites })

def simple_upload(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        return render(request, 'core/simple_upload.html', {
            'uploaded_file_url': uploaded_file_url
        })
    return render(request, 'core/simple_upload.html')


def model_form_upload(request):
    if request.method == 'POST':
        form = SpriteForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = SpriteForm()
    return render(request, 'core/model_form_upload.html', {
        'form': form
    })
