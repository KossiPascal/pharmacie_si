from django.conf.urls import url
from django.contrib import admin
from django.urls import path,include
from django.views.static import serve
from django.conf.urls.static import static
from . import views
from django.conf import settings

handler404 = views.error404
handler500 = views.error500


urlpatterns = [
    path('', views.home, name="home"),
    path('ih_admin/', admin.site.urls),
    path('pharmacy/', include('med.urls')),
    path('auth/', include('auths.urls')),
    path('site/ajax', views.siteAjax, name="site_ajax"),
    path('translation/ajax', views.TranslationAjax, name="translation_ajax"),
]

if settings.DEBUG == False:
    urlpatterns += [
        url(r'^media/(?P<path>.*)$', serve,{'document_root':settings.MEDIA_ROOT}),
        url(r'^static/(?P<path>.*)$', serve,{'document_root':settings.STATIC_DIR}),
    ]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
