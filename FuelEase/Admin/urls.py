from django.urls import path
from Admin import views

app_name = 'Admin'

urlpatterns = [
    path('Admin_home/', views.Admin_Home, name='Admin_home'),
    path('view_registered_pumps/', views.view_registered_pumps, name='view_registered_pumps'),
    path('handle_pump_registration/<int:pump_id>/<str:action>/', views.handle_pump_registration, name='handle_pump_registration'),
    path('most-selling-items/',views.most_selling_items, name='most_selling_items'),
    path('view_admin_profile/', views.view_admin_profile, name='view_admin_profile'),
    path('update_admin_details/', views.update_admin_details, name='update_admin_details'),
    path('change_password/', views.change_password, name='change_password'),
    path('view-complaints/', views.view_complaints, name='view_complaints'),

]