from django.urls import path
from Mechanic import views

app_name = 'Mechanic'

urlpatterns = [
    path('Mechanic_home/', views.Mechanic_home, name='Mechanic_home'),
    path('booking_requests/', views.mechanic_view_booking_requests, name='mechanic_view_booking_requests'),
    path('accept_booking/<int:booking_id>/', views.mechanic_accept_booking, name='mechanic_accept_booking'),
    path('reject_booking/<int:booking_id>/', views.mechanic_reject_booking, name='mechanic_reject_booking'),
    path('mechdetails/', views.mechdetails, name='mechdetails'),
    path('update_details/', views.update_details, name='update_details'),
    path('change_password/', views.change_password, name='change_password'),
    path('mech_complaint/', views.mech_complaint, name='mech_complaint'),
    path('view_replies/', views.ViewReply, name='view_replies'),

]