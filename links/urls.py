from django.urls import path
from . import views

urlpatterns = [
    path('update-db/', views.update_db, name='update_db'),
    path('get-progress/', views.get_progress, name='get_progress'),
    path('search/', views.search_links, name='search_links'),
    path('details/<int:link_id>', views.link_details, name='details'),
    path('connectivity/', views.connectivity_view, name='connectivity'),
    path('get-site-tree/', views.get_site_tree, name='get_site_tree'),
    path('about/', views.about, name='about'),
]
