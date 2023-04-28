from urllib.parse import urlparse

from django.http import HttpResponseRedirect, HttpResponseBadRequest, HttpResponseNotAllowed, HttpResponse, \
    HttpResponseNotFound
from django.shortcuts import render
from django.urls import reverse

from .control import handle_uploaded_file, get_image_file, get_image_file_no_update, track
from .forms import UploadFileForm
from .models import SaveImage


# Create your views here.


def index(request):
    return render(request, "index.html")


def upload(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            name = handle_uploaded_file(request.FILES["file"])
            return HttpResponseRedirect(reverse("image info", args=(name,)))
        return HttpResponseBadRequest()
    else:
        return HttpResponseNotAllowed(['POST'])


def get_image(request, name):
    track(request, name)
    file = None
    try:
        ref = request.headers['Referer']
        url = urlparse(ref)
        if url.netloc == request.get_host():
            file = get_image_file_no_update(name)
    except KeyError:
        pass

    if file is None:
        try:
            file = get_image_file(name)
        except SaveImage.DoesNotExist:
            return HttpResponseNotFound()

    return HttpResponse(file, content_type='image/webp')


def image_info(request, name):
    try:
        img = SaveImage.objects.get(name=name)
    except SaveImage.DoesNotExist:
        return HttpResponseNotFound()
    host = request.get_host()
    file_link = request.scheme + '://' + host + reverse("get image", args=(name,))

    info = {
        'name': name,
        'count': img.count,
        'create': img.create_time,
        'read': img.read_time,
        'info': request.scheme + '://' + host + reverse("image info", args=(name,)),
        'file': file_link,
        'html': f'<img src="{file_link}" alt="{name}.webp" border="0" />',
        'bbcode': f'[img]{file_link}[/img]',
        'markdown': f'![{name}.webp]({file_link})'
    }
    return render(request, "img_info.html", info)
