from django.contrib import admin
from django.urls import path, include  # ✅ Make sure include is imported

urlpatterns = [
    path('admin/', admin.site.urls),          # ✅ Admin route
    path('api/users/', include('users.urls')),  # ✅ Include user-related routes
]
