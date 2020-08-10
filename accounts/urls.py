from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('',views.index, name='index' ),
    path('products/',views.products, name='products' ),
    path('orders/pending',views.pending, name='pending' ),
    path('customer/<int:pk>',views.customers, name='customers' ),

    path('new_order/<int:pk>',views.newOrder, name='new_order' ),
    path('update_order/<int:pk>',views.updateOrder, name='update_order' ),
    path('delete_order/<int:pk>',views.deleteOrder, name='delete_order' ),


    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('register/', views.registerPage, name='register'),

    path('user/', views.user, name='user')



    



]
