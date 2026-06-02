from django.urls import path
from . import views

urlpatterns = [
    path('generate-tspl/', views.generate_tspl_view),
]
