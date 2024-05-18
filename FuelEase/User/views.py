from django.utils import timezone
import math
from urllib import request
from django.http import Http404, HttpResponse, HttpResponseBadRequest, HttpResponseForbidden, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from Admin.models import Admintable
from Pump.models import DeliveryBoy, Fuel, Mechanic, Pump
from User.models import Booking, Complaint, Newuser

def index(request):
    return render(request,'User/index.html')

#//////////////////////////////////////////////////////////////////////////////////

def New_user_register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        password = request.POST.get('password')

        new_user = Newuser(
            username=username,
            email=email,
            phone_number=phone,
            address=address,
            password=password
        )
        new_user.save()
        return redirect('User:login')  
    return render(request, 'User/New_UserReg.html')

# //////////////////////////////////////////////////////////////////////////////////

def login(request):
    if request.method=="POST":
        email=request.POST.get('email')
        password=request.POST.get('password')
        Ulogin=Newuser.objects.filter(email=email,password=password).count()
        Plogin=Pump.objects.filter(email=email,password=password,vstatus=True).count()
        Alogin=Admintable.objects.filter(admin_email=email,admin_password=password).count()
        Dlogin=DeliveryBoy.objects.filter(email=email,password=password).count()
        Mlogin=Mechanic.objects.filter(email=email,password=password).count()


        if Ulogin > 0:
            uadmin=Newuser.objects.get(email=email,password=password)
            request.session['uid']=uadmin.id
            return redirect('User:user_home')
        elif Plogin > 0:
            padmin=Pump.objects.get(email=email,password=password,vstatus=1)
            request.session['pid']=padmin.id
            return redirect('Pump:Pump_home')
        elif Alogin > 0:
            aadmin=Admintable.objects.get(admin_email=email,admin_password=password)
            request.session['aid']=aadmin.id
            return redirect('Admin:Admin_home')
        elif Dlogin > 0:
            dadmin=DeliveryBoy.objects.get(email=email,password=password)
            request.session['did']=dadmin.id
            return redirect('DeliveryBoy:Deliveryboy_home')
        elif Mlogin > 0:
            madmin=Mechanic.objects.get(email=email,password=password)
            request.session['mid']=madmin.id
            return redirect('Mechanic:Mechanic_home')
        else:
            error="Invalid Credentials!!"
            return render(request,"User/Login.html",{'ERR':error})
    else:
        return render(request, "User/Login.html")
    
    #///////////////////////////////////////////////////////

def User_home(request):
    current_user_id = request.session.get('uid')
    if current_user_id:
        user = get_object_or_404(Newuser, pk=current_user_id)
        
        booking = Booking.objects.filter(user=user).first()
        
        return render(request, 'User/Home.html', {'user': user, 'booking': booking})
    else:
        return render(request, 'User/Login.html')


#///////////////////////////////////////////////////////////

def nearest_pumps(request):
    user_lat_str = request.session.get('user_lat')
    user_lon_str = request.session.get('user_lon')

    if user_lat_str is None or user_lon_str is None:
        return render(request, 'User/Error.html', {'message': 'Latitude and/or longitude not provided.'})

    try:
        user_lat = float(user_lat_str)
        user_lon = float(user_lon_str)
    except ValueError:
        return render(request, 'User/Error.html', {'message': 'Invalid latitude and/or longitude format.'})

    pumps = Pump.objects.filter(vstatus=1)
    nearby_pumps = []
    for pump in pumps:
        pump_distance = get_distance(user_lat, user_lon, pump.latitude, pump.longitude)
        if pump_distance <= 50: 
            pump.distance = pump_distance
            nearby_pumps.append(pump)

    return render(request, 'User/Nearby_Pumps.html', {'pumps': nearby_pumps})


def get_distance(lat1, lon1, lat2, lon2):
    R = 6371 
    dLat = math.radians(lat2 - lat1)
    dLon = math.radians(lon2 - lon1)
    a = (
        math.sin(dLat/2) * math.sin(dLat/2) +
        math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * 
        math.sin(dLon/2) * math.sin(dLon/2)
    )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    distance = R * c
    return distance


def set_location(request):
    lat = request.GET.get('lat')
    lon = request.GET.get('lon')
    
    if lat is not None and lon is not None:
        request.session['user_lat'] = lat
        request.session['user_lon'] = lon
        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Latitude and/or longitude not provided.'})
    
    
#///////////////////////////////////////////////////////////////////////////////////

def Error(request):
    return render(request,'User/Error.html')

#//////////////////////////////////////////////////////////////////////////////////


def booknow(request, pump_id):
    if request.method == 'POST':
        pump_id = request.POST.get('pump_id')
        fuel_id = request.POST.get('fuel')
        quantity = int(request.POST.get('quantity'))
        mechanic_needed_str = request.POST.get('mechanic_needed', 'false') 
        mechanic_needed = mechanic_needed_str.lower() == 'true'

        pump = get_object_or_404(Pump, id=pump_id)
        fuel = get_object_or_404(Fuel, id=fuel_id)

        fuel_quantity = int(fuel.quantity)

        if quantity > fuel_quantity:
            return redirect('User:booking_details')

        user_id = request.session.get('uid')

        if user_id:
            user = get_object_or_404(Newuser, id=user_id)
        else:
            error_message = "User not logged in."
            return render(request, 'User/error.html', {'error_message': error_message})

        total_cost = fuel.price * quantity

        payment_status = False
        delivery_boy_contacted = False

        booking = Booking.objects.create(
            user=user,
            pump=pump,
            fuel=fuel,
            quantity=quantity,
            total_cost=total_cost,
            status='Pending',
            mechanic_needed=mechanic_needed,
            payment_status=payment_status,  
            delivery_boy_contacted=delivery_boy_contacted  
        )

        fuel.quantity = str(fuel_quantity - quantity)
        fuel.save()

        return redirect('User:booking_details')

    else:
        pump = get_object_or_404(Pump, id=pump_id)
        return render(request, 'User/User_Book_Fuels.html', {'pump': pump})


#///////////////////////////////////////////////////////////////////////////////////

def booking_details_view(request):
    current_user_id = request.session.get('uid')
    if current_user_id:
        user_bookings = Booking.objects.filter(user_id=current_user_id)
        return render(request, 'User/booking_details.html', {'user_bookings': user_bookings})
    else:
        return HttpResponse("You need to be logged in to view booking details.")
    
#///////////////////////////////////////////////////////////////////////////////////////////

def Payment(request, booking_id):
    current_user_id = request.session.get('uid')
    if not current_user_id:
        return redirect('User:login') 

    user = get_object_or_404(Newuser, pk=current_user_id)
    booking = get_object_or_404(Booking, id=booking_id, user=user, payment_status=False)

    if request.method == 'POST':
        booking.payment_status = True
        booking.save()

        return redirect('User:user_home')

    return render(request, 'User/Payment.html', {'user': user, 'booking': booking})

#//////////////////////////////////////////////////////////////////////////////////////////////

def userdetails(request):
    uid = request.session.get("uid")
    if uid is None:
        return render(request, "User/error.html", {"error_message": "User ID not found in session."})
    
    try:
        user = Newuser.objects.get(id=uid)
    except Newuser.DoesNotExist:
        return render(request, "User/error.html", {"error_message": "User does not exist."})
    
    return render(request, "User/view_profile.html", {"details": user})

def update_profile(request):
    uid = request.session.get("uid")
    if uid is None:
        return render(request, "User/error.html", {"error_message": "User ID not found in session."})

    try:
        userupd = Newuser.objects.get(id=uid)
    except Newuser.DoesNotExist:
        return render(request, "User/error.html", {"error_message": "User does not exist."})

    if request.method == "POST":
        userupd.username = request.POST.get("txt_username")
        userupd.email = request.POST.get("txt_email")
        userupd.phone_number = request.POST.get("txt_phone_number")
        userupd.address = request.POST.get("txt_address")        
        userupd.save()
        return redirect('User:profile')
    
    return render(request, "User/update_profile.html", {"userupd": userupd})

def update_password(request):
    uid = request.session.get("uid")
    if uid is None:
        return render(request, "User/error.html", {"error_message": "User ID not found in session."})

    try:
        user = Newuser.objects.get(id=uid)
    except Newuser.DoesNotExist:
        return render(request, "User/error.html", {"error_message": "User does not exist."})

    if request.method == "POST":
        current_password = request.POST.get("current_password")
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")

        if not user.password == current_password:
            return render(request, "User/error.html", {"error_message": "Incorrect current password."})

        if new_password != confirm_password:
            return render(request, "User/error.html", {"error_message": "New passwords do not match."})

        user.password = new_password
        user.save()

        return redirect('User:user_home')  

    return render(request, "User/update_password.html", {"user": user})

#///////////////////////////////////////////////////////////////////////////////////////////

def submit_complaint(request):
    if request.method == 'POST':
        subject = request.POST.get('subject')
        description = request.POST.get('description')

        if 'uid' in request.session:
            user_id = request.session['uid']
            complaint = Complaint.objects.create(
                user_id=user_id,
                subject=subject,
                description=description,
                created_at=timezone.now()
            )
            return redirect('User:user_home')
        else:
            return render(request, 'error.html', {'error_message': 'User not logged in.'})
    return render(request, 'User/complaint_form.html')


#///////////////////////////////////////////////////////////////////////////////////////

def ViewReply(request):
    current_user_id = request.session.get('uid')
    if current_user_id:
        user_complaints = Complaint.objects.filter(user_id=current_user_id)
        return render(request, 'User/view_replies.html', {'user_complaints': user_complaints})
    else:
        return render(request, 'error.html', {'error_message': 'User not logged in.'})
    
#///////////////////////////////////////////////////////////////////////////////////

def about(request):
    return render(request,'User/about.html')

def complaintdemo(request):
    return render(request,'User/DemoComplaint.html')