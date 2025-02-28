from django.urls import path, include
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)
from rest_framework.routers import DefaultRouter

from order.views.api_views import OrderViewSet, DishViewSet

api_router = DefaultRouter()

api_router.register(r"orders", OrderViewSet)
api_router.register(r"dishes", DishViewSet)


urlpatterns = [
    path("", include(api_router.urls)),
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "swagger/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path("redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
]
