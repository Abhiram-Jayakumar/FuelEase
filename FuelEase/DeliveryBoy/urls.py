from django.urls import path
from DeliveryBoy import views

app_name = 'DeliveryBoy'

urlpatterns = [
    path('Deliveryboy_home/',views.DelveryBoy_Home,name="Deliveryboy_home"),
    path('view_booking_requests/', views.view_booking_requests, name='view_booking_requests'),
    path('accept_booking/<int:booking_id>/', views.accept_booking, name='accept_booking'),
    path('reject_booking/<int:booking_id>/', views.reject_booking, name='reject_booking'),
    path('contacted/<int:booking_id>/', views.contacted, name='contacted'),
    path('deldetails/',views.deldetails,name="deldetails"),
    path('update_delivery_boy/',views.update_delivery_boy,name="update_delivery_boy"),
    path('change_password/',views.change_password,name="change_password"),
    path('mech_complaint/',views.mech_complaint,name="mech_complaint"),
    path('view_replies/', views.ViewReply, name='view_replies'),

]