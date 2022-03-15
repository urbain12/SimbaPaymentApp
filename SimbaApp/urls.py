from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path,include


urlpatterns = [
    path('', include('Payments.urls')),
    path('admin/', admin.site.urls),
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

handle404 = "users.view.page_not_found_view"
handle500 = "users.view.error_to_be_found"
