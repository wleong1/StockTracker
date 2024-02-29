from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('graph', views.update_graph, name="graph"),
    path('price', views.update_price, name="price"),
    path('news', views.update_news, name="news"),
]
