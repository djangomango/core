from django.shortcuts import get_object_or_404, redirect

from apps.attachment.models import FileAttachment, ImageAttachment


def file_attachment(request, uuid):
    file = get_object_or_404(FileAttachment, uuid=uuid)
    return redirect(file.get_absolute_url())


def image_attachment(request, uuid):
    image = get_object_or_404(ImageAttachment, uuid=uuid)
    return redirect(image.get_absolute_url())
