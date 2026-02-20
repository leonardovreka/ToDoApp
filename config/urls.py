from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from todolist.views import TodoViewSet, RegistrationView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)

router = DefaultRouter()
router.register(r'todos', TodoViewSet, basename='todo')

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/', include([
        path('', include(router.urls)),

        #Authentication
        path('auth/register/', RegistrationView.as_view(), name='register'),
        path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain'),
        path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
        path('auth/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    ])),

    #API docs
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
