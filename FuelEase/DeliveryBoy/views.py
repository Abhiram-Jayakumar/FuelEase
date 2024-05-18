from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from DeliveryBoy.models import DeliveryBoyComplaint
from Pump.models import DeliveryBoy
from User.models import Booking

def DelveryBoy_Home(request):
    delivery_boy_id = request.session.get('did') 
    
    if delivery_boy_id:
        delivery_boy = DeliveryBoy.objects.get(pk=delivery_boy_id)
        return render(request,'DeliveryBoy/DeliveryBoy_Home.html', {'delivery_boy': delivery_boy})
    else:
        return render(request, 'DeliveryBoy/DeliveryBoy_Home.html')
#//////////////////////////////////////////////////////////////////

def view_booking_requests(request):
    current_delivery_boy_id = request.session.get('did') 
    if current_delivery_boy_id:
        booking_requests = Booking.objects.filter(delivery_boy_id=current_delivery_boy_id)
        return render(request, 'DeliveryBoy/Booking_Requests.html', {'booking_requests': booking_requests})
    else:
        return render(request, 'DeliveryBoy/Booking_Requests.html')

def accept_booking(request, booking_id):
    if request.method == 'POST':
        booking = get_object_or_404(Booking, id=booking_id)
        booking.status = 'Accepted'
        booking.save()
        return redirect('DeliveryBoy:view_booking_requests')
    else:
        return HttpResponseBadRequest("Invalid request method")

def reject_booking(request, booking_id):
    if request.method == 'POST':
        booking = get_object_or_404(Booking, id=booking_id)
        booking.status = 'Rejected'
        booking.save()
        return redirect('DeliveryBoy:view_booking_requests')
    else:
        return HttpResponseBadRequest("Invalid request method")
    
    
def contacted(request, booking_id):
    if request.method == 'POST':
        booking = get_object_or_404(Booking, id=booking_id)        
        booking.delivery_boy_contacted = True
        booking.save()
        return redirect('DeliveryBoy:view_booking_requests')
    else:
        return HttpResponseBadRequest("Invalid request method")
    
    
#////////////////////////////////////////////////////////////////////////////////

def deldetails(request):
    did = request.session.get("did")
    if did is None:
        return render(request, "User/Error.html", {"error_message": "User ID not found in session."})
    
    try:
        deliver_boy = DeliveryBoy.objects.get(id=did)
    except DeliveryBoy.DoesNotExist:
        return render(request, "User/Error.html", {"error_message": "User does not exist."})
    return render(request, "DeliveryBoy/profile.html", {"delivery_boy": deliver_boy})    


def update_delivery_boy(request):
    did = request.session.get('did')
    if did:
        delivery_boy = get_object_or_404(DeliveryBoy, id=did)
        if request.method == 'POST':
            delivery_boy.name = request.POST.get('name')
            delivery_boy.phone_number = request.POST.get('phone_number')
            delivery_boy.license_number = request.POST.get('license_number')
            delivery_boy.address = request.POST.get('address')
            delivery_boy.email = request.POST.get('email')
            delivery_boy.save()
            return redirect('DeliveryBoy:Deliveryboy_home')
        else:
            return render(request, 'DeliveryBoy/delivery_boy_update.html', {'delivery_boy': delivery_boy})
    else:
        return redirect('DeliveryBoy:Deliveryboy_home')
    
    
def change_password(request):
    if request.method == 'POST':
        did = request.session.get('did')  
        if did:
            delivery_boy = get_object_or_404(DeliveryBoy, id=did)
            new_password = request.POST.get('new_password')
            delivery_boy.password = new_password
            delivery_boy.save()
            return redirect('DeliveryBoy:Deliveryboy_home')
    return render(request, 'DeliveryBoy/change_password.html')

#/////////////////////////////////////////////////////////////////

def mech_complaint(request):
    if request.method == 'POST':
        title = request.POST.get('subject')
        description = request.POST.get('description')

        if 'did' in request.session:
            del_id = request.session['did']
            delivery_boy = DeliveryBoy.objects.get(id=del_id)
            complaint = DeliveryBoyComplaint.objects.create(
                delivery_boy=delivery_boy,
                title=title,
                description=description,
                created_at=timezone.now()
            )
            return redirect('DeliveryBoy:Deliveryboy_home')
        else:
            return render(request, 'User:Error.html', {'error_message': 'User not logged in.'})
    return render(request, 'DeliveryBoy/complaint.html')

#//////////////////////////////////////////////////////////////////////////////////

def ViewReply(request):
    current_deliveryboy_id = request.session.get('did')
    if current_deliveryboy_id:
        deliveryboy_complaints = DeliveryBoyComplaint.objects.filter(delivery_boy_id=current_deliveryboy_id)
        return render(request, 'DeliveryBoy/view_replies.html', {'deliveryboy_complaints': deliveryboy_complaints})
    else:
       
        return render(request, 'error.html', {'error_message': 'Delivery boy not logged in.'})


 