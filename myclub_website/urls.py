from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('events.urls')),
    path('members/', include('django.contrib.auth.urls')),
    path('members/', include('members.urls')),
]

admin.site.site_header = "Administration Database"
admin.site.site_title = "Administration Database"
admin.site.index_title = "Database"