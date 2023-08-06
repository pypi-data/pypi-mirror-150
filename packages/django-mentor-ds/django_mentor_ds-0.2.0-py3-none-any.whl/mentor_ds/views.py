from django.shortcuts import render
from appointment.templatetags.appointment_tags import make_post_context
from _data import context

import logging
logger = logging.getLogger(__name__)
formatter = logging.Formatter('%(levelname)s: [%(name)s] %(message)s')
ch = logging.StreamHandler()
ch.setFormatter(formatter)
logger.addHandler(ch)
logger.setLevel(logging.INFO)


def buildup(request):
    c = context.context
    logger.debug(c)
    if request.method == 'GET':
        return render(request, f"mentor_ds/base.html", c)
    elif request.method == "POST":
        # appointment가 contact에 포함된 경우는 anchor를 contact으로 설정한다.
        c.update(make_post_context(request.POST, c['basic_info']['consult_email'], anchor='contact'))
        return render(request, f"mentor_ds/base.html", c)
