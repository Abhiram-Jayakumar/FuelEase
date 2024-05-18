from django.urls import path
from Pump import views

app_name = 'Pump'

urlpatterns = [
    path('Pump_home/', views.Pump_home, name='Pump_home'),
    path('pump_register/', views.pump_register, name='pump_register'),
    path('add_fuel/', views.add_fuel, name='add_fuel'),
    path('add_mechanic/', views.add_mechanic, name='add_mechanic'),
    path('view_pump_mechanics/', views.view_pump_mechanics, name='view_pump_mechanics'),
    path('remove_mechanic/<int:mechanic_id>/', views.remove_mechanic, name='remove_mechanic'),
    path('Add_deliveryboy/', views.Add_deliveryboy, name='Add_deliveryboy'),
    path('view_pump_delivery_boys/', views.view_pump_delivery_boys, name='view_pump_delivery_boys'),
    path('remove_delivery_boy/<int:deliveryboy_id>/', views.remove_delivery_boy, name='remove_delivery_boy'),
    path('view_pump_fuels/', views.view_pump_fuels, name='view_pump_fuels'),
    path('view_booking_requests/', views.view_booking_requests, name='view_booking_requests'),
    path('assign_mechanic/<int:booking_id>/', views.assign_mechanic, name='assign_mechanic'),
    path('assign_delivery_boy/<int:booking_id>/', views.assign_delivery_boy, name='assign_delivery_boy'),
    path('accept_booking/<int:booking_id>/', views.accept_booking, name='accept_booking'),
    path('reject_booking/<int:booking_id>/', views.reject_booking, name='reject_booking'),
    path('profile/', views.profile, name='profile'),
    path('update_details/', views.update_pump_details, name='update_pump_details'),
    path('change_password/', views.change_pump_password, name='change_pump_password'),
    path('pump_complaint/', views.pump_complaint, name='pump_complaint'),
    path('view_replies/', views.ViewReply, name='view_replies'),
    path('edit_fuel/<int:pump_id>/<int:fuel_id>/', views.edit_fuel, name='edit_fuel'),



]