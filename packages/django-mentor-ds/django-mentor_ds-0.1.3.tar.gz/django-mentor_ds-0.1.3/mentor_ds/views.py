import pickle
from django.shortcuts import render
from django.conf import settings
from appointment.templatetags.appointment_tags import make_post_context

import logging
logger = logging.getLogger(__name__)
formatter = logging.Formatter('%(levelname)s: [%(name)s] %(message)s')
ch = logging.StreamHandler()
ch.setFormatter(formatter)
logger.addHandler(ch)
logger.setLevel(logging.INFO)


def buildup(request):
    # 상부 프로젝트에서 저장해둔 context 피클을 불러와서 context로 저장한다.
    with open(settings.DATA_PATH, 'rb') as fr:
        context = pickle.load(fr)
    if request.method == 'GET':
        return render(request, f"mentor_ds/base.html", context)
    elif request.method == "POST":
        context.update(make_post_context(request.POST, 'hj3415@gmail.com'))
        return render(request, f"mentor_ds/base.html", context)
