from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'products', views.ProductViewSet)

urlpatterns = [
    path('generate-tspl/', views.generate_tspl_view),
    path('sign/', views.sign_qz),
    path('', include(router.urls)),
]

