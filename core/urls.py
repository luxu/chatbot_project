from django.urls import path

from core import views

urlpatterns = [
    path('', views.index, name='index'),
    path('upload_pdf/', views.upload_pdf, name='upload_pdf'),
    path('answer/', views.answer, name='answer')
]
