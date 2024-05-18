from django.urls import path
from User import views

app_name = 'User'

urlpatterns = [
        path('index/', views.index, name='index'),
        path('user_register/', views.New_user_register, name='user_register'),
        path('login/', views.login, name='login'),
        path('user_home/', views.User_home, name='user_home'),
        path('nearest_pumps/',views.nearest_pumps, name='nearest_pumps'),
        path('Error/', views.Error, name='Error'),
        path('set_location/', views.set_location, name='set_location'),
        path('booknow/<int:pump_id>/', views.booknow, name='booknow'),
        path('booking/', views.booking_details_view, name='booking_details'),
        path('Payment/<int:booking_id>/', views.Payment, name='Payment'),  
        path('profile/', views.userdetails, name='profile'),
        path('update_profile/', views.update_profile, name='update_profile'),
        path('update_password/', views.update_password, name='update_password'),
        path('Complaint/', views.submit_complaint, name='Complaint'),
        path('view_replies/', views.ViewReply, name='view_replies'),
        path('about/', views.about, name='about'),
        path('complaintdemo/', views.complaintdemo, name='complaintdemo'),
        
]