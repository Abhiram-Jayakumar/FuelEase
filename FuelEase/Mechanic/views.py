from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render
from Mechanic.models import MechanicComplaint
from Pump.models import Mechanic
from User.models import Booking
from django.utils import timezone



def Mechanic_home(request):
    mid = request.session.get("mid")
    mechnaic = Mechanic.objects.get(id=mid)
    return render(request,'Mechanic/Mechanic_Home.html', {"mechanic": mechnaic})

#//////////////////////////////////////////////////////////////

def mechanic_view_booking_requests(request):
    if request.method == 'GET':
        mechanic_id = request.session.get('mid')
        
        if mechanic_id:
            booking_requests = Booking.objects.filter(mechanic_id=mechanic_id)
            return render(request, 'Mechanic/View_Booking_Requests.html', {'booking_requests': booking_requests})
        else:
            return HttpResponseBadRequest("Mechanic ID not found in session")
    else:
        return HttpResponseBadRequest("Invalid request method")


def mechanic_accept_booking(request, booking_id):
    if request.method == 'POST':
        booking = get_object_or_404(Booking, id=booking_id)        
        booking.status = 'Accepted'
        booking.save()        
        return redirect('Mechanic:mechanic_view_booking_requests')  
    else:
        return HttpResponseBadRequest("Invalid request method")

def mechanic_reject_booking(request, booking_id):
    if request.method == 'POST':
        booking = get_object_or_404(Booking, id=booking_id)        
        booking.status = 'Rejected'
        booking.save()        
        return redirect('Mechanic:mechanic_view_booking_requests')
    else:
        return HttpResponseBadRequest("Invalid request method")
    
    
#/////////////////////////////////////////////////////////////////////////////////////////


def mechdetails(request):
    mid = request.session.get("mid")
    if mid is None:
        return render(request, "User/Error.html", {"error_message": "User ID not found in session."})
    
    try:
        mechnaic = Mechanic.objects.get(id=mid)
    except Mechanic.DoesNotExist:
        return render(request, "Mechanic/Error.html", {"error_message": "User does not exist."})
    
    return render(request, "Mechanic/M_profile.html", {"mechanic": mechnaic})


def update_details(request):
    if request.method == 'POST':
        mid = request.session.get('mid')
        if mid:
            mechanic = get_object_or_404(Mechanic, id=mid)
            mechanic.name = request.POST.get('name')
            mechanic.phone_number = request.POST.get('phone_number')
            mechanic.email = request.POST.get('email')
            mechanic.address = request.POST.get('address')
            mechanic.save()
            return redirect('Mechanic:Mechanic_home')
        else:
            return redirect('Mechanic:Mechanic_home')  
    else:
        mid = request.session.get('mid')
        if mid:
            mechanic = get_object_or_404(Mechanic, id=mid)
            return render(request, 'Mechanic/update_details.html', {'mechanic': mechanic})
        else:
            return redirect('Mechanic:Mechanic_home')  

def change_password(request):
    if request.method == 'POST':
        mid = request.session.get('mid')
        if mid:
            mechanic = get_object_or_404(Mechanic, id=mid)
            new_password = request.POST.get('new_password')
            mechanic.password = new_password  
            mechanic.save()
            return redirect('Mechanic:Mechanic_home')
        else:
            return redirect('Mechanic:Mechanic_home')  
    else:
        return render(request, 'Mechanic/change_password.html')
    


#///////////////////////////////////////////////////////////////////////////
    
    
def mech_complaint(request):
    if request.method == 'POST':
        title = request.POST.get('subject')
        description = request.POST.get('description')

        if 'mid' in request.session:
            mech_id = request.session['mid']
            complaint = MechanicComplaint.objects.create(
                mechanic_id=mech_id,
                title=title,
                description=description,
                created_at=timezone.now()
            )
            return redirect('Mechanic:Mechanic_home')
        else:
            return render(request, 'User:Error.html', {'error_message': 'User not logged in.'})
    return render(request, 'Mechanic/Mech_complaint.html')

#////////////////////////////////////////////////////////////////////////////////////////////////////////

def ViewReply(request):
    current_mechanic_id = request.session.get('mid')
    if current_mechanic_id:
        mechanic_complaints = MechanicComplaint.objects.filter(mechanic_id=current_mechanic_id)
        return render(request, 'Mechanic/view_replies.html', {'mechanic_complaints': mechanic_complaints})
    else:
        return render(request, 'error.html', {'error_message': 'Mechanic not logged in.'})
