django-mentor_ds
==========

django-mentor_ds is a Django app to use for demiansoft. 

Quick start
------------

1. 본 템플릿은 다음의 필수 앱들이 필요하다. 프로젝트의 settings.py에 다음을 추가한다.
```python
INSTALLED_APPS = [
    ...
    
    'django.contrib.humanize',
    
    'mentor_ds',
    
    # 필수 컴포넌트
    'popup',
    'base',
    'home',
    'hero',
    
    # 선택 공통 컴포넌트
    'counts',
    'about',
    'whyus',
    'testimonials',
    'team',
    'faq',
    'contact',
    'appointment',  # contact에서 내부적으로 사용함
    
    # 선택 유니크 컴포넌트
    'courses',
    'features',
    'events',
    'pricing',
]
```

2. 프로젝트의 urls.py에 다음을 추가한다.
```python
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # ...
    path('', include('home.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```


