from django.template import Library
from ..models import NotiPopup, EventPopup, ImagePopup

import logging
logger = logging.getLogger(__name__)
formatter = logging.Formatter('%(levelname)s: [%(name)s] %(message)s')
ch = logging.StreamHandler()
ch.setFormatter(formatter)
logger.addHandler(ch)
logger.setLevel(logging.ERROR)


register = Library()

# https://localcoder.org/django-inclusion-tag-with-configurable-template


@register.inclusion_tag(f"popup/popup.html")
def make_popup():
    noti_popup = NotiPopup.objects
    event_popup = EventPopup.objects
    image_popup = ImagePopup.objects
    context = {'noti_popup': noti_popup, 'event_popup': event_popup, 'image_popup': image_popup}
    logger.info(context)
    return context
