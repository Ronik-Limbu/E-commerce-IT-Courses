from django.urls import path
from django.contrib.auth import views as auth_views
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('contact/', contact, name='contact'),
    path('About_us/',About_us,name='About_us'),
    path('all_courses/', all_courses, name='all_courses'),
    path('search/', search_form, name='search_form'),
    path('verify_certificate/', verify_certificate, name="verify_certificate"),
    path('certificate_detail/', verify_certificate, name="certificate_detail"),
    path('register/', register,name='register'),
    path('log_in/', log_in,name='log_in'),
    path('log_out/', log_out,name='log_out'),
    path("product_detail/<int:id>",product_detail,name="product_detail"),
    path('profile/',customer_profile,name='profile'),
    path('change_password/', auth_views.PasswordChangeView.as_view(template_name='auth/change_password.html'), name='change_password'),

#    change password
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='auth/password_reset.html'),name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name='auth/password_reset_done.html'), name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='auth/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='auth/password_reset_complete.html'), name='password_reset_complete'),
   

# reviews and rating
    path('courses_reviews/<int:id>', course_reviews, name='course_reviews'),
 
#   cart system
    path('cart/', cart_detail, name='cart_detail'),
    path('cart/remove/<int:id>/', item_clear, name='cart_remove'),
    path('cart/add/<int:id>/', cart_add, name='cart_add'),
    path('cart/item_clear/<int:id>/', item_clear, name='item_clear'),
    path('cart/item_increment/<int:id>/', item_increment, name='item_increment'),
    path('cart/item_decrement/<int:id>/', item_decrement, name='item_decrement'),
    path('cart/clear/', cart_clear, name='cart_clear'),
    path('cart/detail/', cart_detail, name='cart_detail'),

#check out
    path('orders_list/', orders_list, name="orders_list"),
    path('create_order/', create_order, name="create_order"),
    path('order_remove/<int:id>/', order_remove, name="order_remove"),
    path('checkout/<int:id>/', order_checkout, name="order_checkout"),
    path('esewa_callback/', esewa_callback, name="esewa_callback"),
    path('payment_failed/', payment_failed, name="payment_failed"),
] 