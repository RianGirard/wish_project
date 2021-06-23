from django.urls import path
from . import views 

urlpatterns = [
    path ('', views.index),
    path ('login', views.login),
    path ('logout', views.logout),
    path ('register', views.register),
    path ('success', views.success),
    path ('email_valid/', views.email_valid_null),       # this is here for case of zero text value entry
    path ('email_valid/<str:email>', views.email_valid),
    path ('email_regex/', views.email_regex_null),
    path ('email_regex/<str:email>', views.email_regex),
    path ('wishes', views.wishes),
    path ('wishes/new', views.wishes_new), 
    path ('wishes/create_wish', views.create_wish),
    path ('wishes/destroy/<int:id>', views.destroy_wish),
    path ('wishes/edit/<int:id>', views.wish_edit),
    path ('wishes/edit/update_wish', views.update_wish),
    path ('wishes/edit/logout', views.logout),
    path ('wishes/grant/<int:id>', views.grant_wish),
    path ('wishes/like/<int:id>', views.like_wish),
    path ('wishes/stats', views.stats),
    path ('wishes/logout', views.logout),
]