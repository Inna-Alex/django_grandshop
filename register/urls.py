from django.contrib import admin
from django.urls import include, path
from register import views as v

urlpatterns = [
    path('admin/', admin.site.urls),
    path("register/", v.register, name="register"),  # <-- added
    path('', include("main.urls")),
]
