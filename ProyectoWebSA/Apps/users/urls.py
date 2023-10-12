from django.urls import path

from . import views

app_name = "Apps.users"
urlpatterns = [
     path('', views.UsersListView, name='users_list'),
     path('add', views.UsersAddView, name='users_add'),
     path('delete/<str:user_id>',
          views.UsersDeleteView, name='users_delete'),
     path('update/<str:user_id>/<str:userdate_id>/',
          views.UsersUpdateView, name='users_update'), 
     path('pay/<str:user_id>/<str:userdate_id>/',
          views.UsersPayView, name='users_pay'),
     path('pago/', views.PayListView, name='pay_list'),   
]
