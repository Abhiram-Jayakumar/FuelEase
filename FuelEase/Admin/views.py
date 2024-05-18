from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from Admin.models import Admintable
from DeliveryBoy.models import DeliveryBoyComplaint
from Mechanic.models import MechanicComplaint
from Pump.models import DeliveryBoy, Mechanic, Pump, PumpComplaint
from User.models import Booking, Complaint, Newuser
from django.db.models import Sum


def Admin_Home (request):
   user_count = Newuser.objects.count()
   pump_count = Pump.objects.count()
   mechanic_count = Mechanic.objects.count()
   delivery_boy_count = DeliveryBoy.objects.count()

   return render(request, 'Admin/Admin_Home.html', {
        'user_count': user_count,
        'pump_count': pump_count,
        'mechanic_count': mechanic_count,
        'delivery_boy_count': delivery_boy_count,
    })
#////////////////////////////////////////////////////////////////

def view_registered_pumps(request):
    registered_pumps = Pump.objects.filter(vstatus=0)

    return render(request, 'Admin/view_registered_pumps.html', {'registered_pumps': registered_pumps})

#//////////////////////////////////////////////////////////////////////////////////////

def handle_pump_registration(request, pump_id, action):
    pump = get_object_or_404(Pump, pk=pump_id)

    if action == 'accept':
        pump.vstatus = 1 
    elif action == 'reject':
        pump.vstatus = -1 
    else:
        return redirect('Admin:view_registered_pumps')
    pump.save()
    return redirect('Admin:view_registered_pumps')

#//////////////////////////////////////////////////////////////////////////////

def most_selling_items(request):
    sales_data = Booking.objects.values('fuel__fuel_type').annotate(total_quantity=Sum('quantity')).order_by('-total_quantity')

    return render(request, 'Admin/most_selling_items.html', {'sales_data': sales_data})

#////////////////////////////////////////////////////////////////////////////////////
def view_admin_profile(request):
    admin = Admintable.objects.first() 
    return render(request, 'Admin/view_admin_profile.html', {'admin': admin})

#//////////////////////////////////////////////////////////////////////////////////

def update_admin_details(request):
    if request.method == 'POST':
        admin = Admintable.objects.first()  
        admin.admin_name = request.POST.get('admin_name')
        admin.admin_email = request.POST.get('admin_email')
        admin.save()
        return redirect('Admin:view_admin_profile')
    else:
        admin = Admintable.objects.first()  
        return render(request, 'Admin/update_admin_details.html', {'admin': admin})

def change_password(request):
    if request.method == 'POST':
        admin = Admintable.objects.first() 
        new_password = request.POST.get('new_password')
        admin.admin_password = new_password 
        admin.save()
        return redirect('Admin:view_admin_profile')
    else:
        return render(request, 'Admin/change_password.html')
    
#///////////////////////////////////////////////////////////////////////////////////////////

def view_complaints(request):
    if request.method == 'POST':
        complaint_type = request.POST.get('complaint_type')
        complaint_id = request.POST.get('complaint_id')
        admin_reply = request.POST.get('admin_reply')

        if complaint_type == 'user':
            complaint = Complaint.objects.get(id=complaint_id)
            complaint.admin_reply = admin_reply
            complaint.save()
        elif complaint_type == 'pump':
            complaint = PumpComplaint.objects.get(id=complaint_id)
            complaint.admin_reply = admin_reply
            complaint.save()
        elif complaint_type == 'mechanic':
            complaint = MechanicComplaint.objects.get(id=complaint_id)
            complaint.admin_reply = admin_reply
            complaint.save()
        elif complaint_type == 'delivery_boy':
            complaint = DeliveryBoyComplaint.objects.get(id=complaint_id)
            complaint.admin_reply = admin_reply
            complaint.save()

        messages.success(request, 'Reply submitted successfully!')
        return redirect('Admin:view_complaints')

    user_complaints = Complaint.objects.all()
    pump_complaints = PumpComplaint.objects.all()
    mechanic_complaints = MechanicComplaint.objects.all()
    delivery_boy_complaints = DeliveryBoyComplaint.objects.all()

    return render(request, 'Admin/view_complaints.html', {
        'user_complaints': user_complaints,
        'pump_complaints': pump_complaints,
        'mechanic_complaints': mechanic_complaints,
        'delivery_boy_complaints': delivery_boy_complaints,
    })