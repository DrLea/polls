from django.urls import path

from . import views

app_name = 'polls'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/details', views.DetailView.as_view(), name = 'detail'),
    path('<int:pk>/results', views.ResultsView.as_view(), name = 'results'),
    path('<int:question_id>/vote', views.vote, name = 'vote'),
    path('<int:question_id>/results/json', views.results, name = 'results.json')
]