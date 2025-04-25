from django.urls import path
from . import views


urlpatterns = [
    path('', views.landing_page, name='landing'),

    # 🔹 Redirect after login based on role:
    path('home/', views.user_home, name='user_home'),  # For regular users
    path('manager/', views.manager_home, name='manager_home'),  # For managers
    
    path('cafes/', views.cafe_list, name='cafe_list'),
    
    path('manager/cafes/', views.manager_cafes, name='manager_cafes'),
    path('manager/cafes/add/', views.add_cafe, name='add_cafe'),
    path('manager/cafes/edit/<int:cafe_id>/', views.edit_cafe, name='edit_cafe'),
    
    path('api/book/', views.api_book_table, name='api_book_table'),
    
    path('book/', views.book_table, name='book_table'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    path('cancel-booking/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),

    path('manager/bookings/', views.manager_bookings, name='manager_bookings'),

    # 🔹 Auth
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]
