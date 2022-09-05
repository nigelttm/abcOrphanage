from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='homepage'),
    path('home', views.home, name='homepage'),
    path('login', views.user_login, name='login'),
    path('logout', views.user_logout, name='logout'),
    path('edit', views.user_edit, name='editAcc'),
    path('register', views.user_register, name='signup'),
    path('donate', views.donate, name='donate'),
    path('works', views.works, name='childrenWork'),
    path('upload', views.uploadWork, name='upload'),
    path('request', views.request, name='request'),
    path('requestCompleted', views.requestCompleted, name='requestCompleted'),
    path('delRequest', views.removeRequest, name='delRequest'),
    path('contact', views.contact, name='contact'),
    path('visit', views.visit, name='visit'),
    path('AccRejVisit', views.AcceptOrRejectVisit, name='AccRejVisit'),
    path('createAcc', views.admin_create, name='adminCreate'),
    path('like/<int:upload_id>', views.like, name='like'),
    path('cancel/<int:md_id>', views.cancel, name='cancel'),
]