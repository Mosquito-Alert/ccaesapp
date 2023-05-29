from django.urls import path
from main import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<str:ccaa>/<int:year>', views.index_par, name='index_par')
]

