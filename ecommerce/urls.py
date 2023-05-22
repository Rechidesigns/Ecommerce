from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
)


urlpatterns = [
    # SWAGGER DOCS UI PATHS
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-schema"),
    path("admin/", admin.site.urls),
    path("__debug__/", include("debug_toolbar.urls")),
        # applications url
    path('store/', include('store.api.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
# urlpatterns = [
#     # applications url
#     path('store/', include('store.api.urls')),
# ]
