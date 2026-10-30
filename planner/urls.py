# planner/urls.py
from django.urls import path
from . import views


app_name = 'planner'

urlpatterns = [
    path('', views.home, name='home'),
    path('plan/', views.plan, name='plan'),
    path('calculate/', views.calculate, name='calculate'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('save-location/', views.save_location, name='save_location'),
    path('get-locations/', views.get_locations, name='get_locations'),
    path(
    "api/agricultural-context/",
    views.agricultural_context_api,
    name="agricultural_context_api"
    ),
    path(
    "api/nlp-query/",
    views.nlp_query_api,
    name="nlp_query_api"

),
    path(
        "api/agro-dealers/",
        views.agro_dealers_api,
        name="agro_dealers_api"
    ),
]