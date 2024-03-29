from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.main, name='main_page'),
    path('tours/', views.tours, name='tours_page'),
    path('tours/direction/<str:country>/', views.tour_country, name='tour_direction'),
    path('tours/review/<int:tour_id>', views.review, name='review'),
    path('profile/', views.profile, name='profile'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup, name='signup'),
    path('tours/reserve/<int:tour_id>/', views.reserve, name='reserve'),
    path('tours/delete_reserve/<int:reserve_id>', views.delete_reserve, name='del_reserve'),
    path('stat/<str:country>', views.stat, name='stat'),
    path('choose_stat/', views.choose_stat, name='choose_stat')
]