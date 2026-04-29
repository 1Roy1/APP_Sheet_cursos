from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    
    # urls de cursos
    path('cursos/', views.curso_list, name='curso_list'),
    path('cursos/nuevo/', views.curso_form, name='curso_create'),
    path('cursos/editar/<str:id>/', views.curso_form, name='curso_edit'),
    path('cursos/eliminar/<str:id>/', views.curso_delete, name='curso_delete'),
    
    # urls de catedraticos
    path('catedraticos/', views.catedratico_list, name='catedratico_list'),
    path('catedraticos/nuevo/', views.catedratico_form, name='catedratico_create'),
    path('catedraticos/editar/<str:id>/', views.catedratico_form, name='catedratico_edit'),
    path('catedraticos/eliminar/<str:id>/', views.catedratico_delete, name='catedratico_delete'),
]
