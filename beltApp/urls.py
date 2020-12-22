from django.urls import path
from . import views

urlpatterns = [

    # -------- Render Routes ----------
    path('', views.index),
    path('dashboard', views.dashboard),
    path('shows/new', views.new_page),
    path('shows/<int:show_id>', views.show_page),
    path('shows/<int:show_id>/edit', views.updateShowDB),
    path('shows/<int:show_id>/updatePage', views.edit_page),


    # -------- Action Routes ----------
    path('register', views.register),
    path('login', views.login),
    path('logout', views.logout),
    #
    path('shows/create', views.create_show),
    path('shows/<int:show_id>/delete', views.delete),

]
