import hashlib
import sys
from io import BytesIO

import base58
from PIL import Image
from django.core.files.images import ImageFile
from django.core.handlers.wsgi import WSGIRequest
from django.utils import timezone

from .models import SaveImage, VisitTrace


def track(request:WSGIRequest, name):
    trace = VisitTrace.objects.create(name=name)
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        trace.ip = x_forwarded_for.split(',')[0]
    else:
        trace.ip = request.META.get('REMOTE_ADDR')
    trace.useragent = request.headers.get('User-Agent')
    trace.referer = request.headers.get('Referer')


def handle_uploaded_file(f) -> str:
    image = Image.open(f)
    mem_buf = BytesIO()
    image.save(mem_buf, format="webp")
    h = hashlib.sha1(mem_buf.getbuffer())
    digest = h.digest()[:4]
    b58 = base58.b58encode(digest)
    name = str(b58, encoding=sys.getfilesystemencoding())[:5]
    filename = name + '.webp'

    save_img, created = SaveImage.objects.get_or_create(name=name)
    if created:
        save_img.file = ImageFile(mem_buf, filename)
        save_img.save()
        print(f'New file {save_img.file}')
    return name


def get_image_file(name):
    save_img = SaveImage.objects.get(name=name)
    save_img.count += 1
    save_img.read_time = timezone.now()
    save_img.save()
    return save_img.file


def get_image_file_no_update(name):
    save_img = SaveImage.objects.get(name=name)
    return save_img.file
