from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('', include('lucros.urls')),
    path("books/", include("lucros.urls")),
    path("template/", include("lucros.urls")),
    path("saldo/", include("lucros.urls")),
    path("admin/", admin.site.urls),
]
