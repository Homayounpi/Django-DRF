from django.urls import path
from . import views


app_name = 'home'
urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('questions/', views.QuestionListView.as_view(), name='question'),
    path('question/create/', views.QuestionCreateView.as_view(), name='question'),
    path('question/update/<int:pk>/', views.QuestionUpdateView.as_view()),
    path('question/delete/<int:pk>/', views.QuestionDeleteView.as_view()),
]
