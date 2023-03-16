from django.urls import path , include
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('signup', views.signup, name='signup'),
    path('signin', views.signin, name='signin'),
    path('signout', views.home, name='signout'),
    path('scrape-data/', views.scrape_data_view, name='scrape-data'),
]
