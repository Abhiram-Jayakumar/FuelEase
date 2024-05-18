from pyexpat.errors import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from Pump.models import DeliveryBoy, Fuel, Mechanic, Pump, PumpComplaint
from User.models import Booking
from django.contrib import messages




def Pump_home(request):
    current_pump_id = request.session.get('pid')
    if current_pump_id:
        pump = get_object_or_404(Pump, pk=current_pump_id)
        return render(request, 'Pump/Pump_Home.html', {'pump': pump})
    else:
        return render(request, 'User/Login.html')

#/////////////////////////////////////////////////////

def pump_register(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        address = request.POST.get('add')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        gst_no = request.POST.get('lic')
        password = request.POST.get('pass')
        lat = request.POST.get('l1')
        lon = request.POST.get('l2')

        if Pump.objects.filter(email=email).exists():
            messages.error(request, 'User with this email already registered.')
            return redirect('pump_register')

        try:
            new_pump = Pump(
                name=name,
                address=address,
                phone_number=phone,
                email=email,
                gst_no=gst_no,
                password=password,
                latitude=lat,
                longitude=lon
            )
            new_pump.save()
        except Exception as e:
            messages.error(request, f'Error occurred: {str(e)}')
        return redirect('User:login')

    return render(request, 'Pump/Pump_Register.html')


#////////////////////////////////////////////////////////////////////////////

def add_fuel(request):
    if request.method == 'POST':
        current_pump_id = request.session.get('pid')

        if current_pump_id:
            fuel_type = request.POST.get('fuelType')
            quantity = request.POST.get('quantity')
            price = request.POST.get('price')

            pump = get_object_or_404(Pump, pk=current_pump_id)

            fuel = Fuel.objects.create(
                fuel_type=fuel_type,
                quantity=quantity,
                price=price,
                pumpId=pump
            )

            return redirect('Pump:view_pump_fuels')  
        else:
            return redirect('Pump:view_pump_fuels')

    return render(request, 'Pump/Add_Product.html')
#////////////////////////////////////////////////////////////////////////////////////

def view_pump_fuels(request):
    current_pump_id = request.session.get('pid')
    if current_pump_id:
        pump = get_object_or_404(Pump, pk=current_pump_id)
        fuels = Fuel.objects.filter(pumpId=pump).order_by('-id')
        context = {
            'fuels': fuels,
            'pump': pump
        }
        return render(request, 'Pump/View_Pump_Fuels.html', context)
    else:
        return redirect('Pump:add_fuel')


    
#//////////////////////////////////////////////////////////////////////////////////

def add_mechanic(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        password = request.POST.get('password')
        pump_id = request.session.get('pid')

        if pump_id:
            try:
                pump = Pump.objects.get(pk=pump_id)
                new_mechanic = Mechanic(
                    name=name,
                    address=address,
                    phone_number=phone,
                    email=email,
                    password=password,
                    pumpId=pump
                )
                new_mechanic.save()
                return redirect('Pump:view_pump_mechanics')  
            except Pump.DoesNotExist:
                return redirect('Pump:view_pump_mechanics')  
        else:
            return redirect('Pump:view_pump_mechanics')  

    return render(request, 'Pump/Add_Mechanic.html')


#/////////////////////////////////////////////////////////////////////////////////

def view_pump_mechanics(request):
    pump_id = request.session.get('pid')
    if pump_id:
        try:
            pump = Pump.objects.get(pk=pump_id)
            mechanics = Mechanic.objects.filter(pumpId=pump)
            return render(request, 'Pump/View_Pump_Mechanics.html', {'mechanics': mechanics})
        except Pump.DoesNotExist:
            return redirect('Pump:add_mechanic')  
    else:
        return redirect('Pump:add_mechanic')  


def remove_mechanic(request, mechanic_id):
    mechanic = get_object_or_404(Mechanic, pk=mechanic_id)
    mechanic.delete()
    return redirect('Pump:view_pump_mechanics')

#/////////////////////////////////////////////////////////////////////////////////////////////////////////

def Add_deliveryboy(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        password = request.POST.get('password')
        license_number = request.POST.get('license')
        pump_id = request.session.get('pid')

        if pump_id:
            try:
                pump = Pump.objects.get(pk=pump_id)
                new_deliveryboy = DeliveryBoy(
                    name=name,
                    address=address,
                    phone_number=phone,
                    email=email,
                    password=password,
                    license_number=license_number,
                    pumpId=pump
                )
                new_deliveryboy.save()
                return redirect('Pump:view_pump_delivery_boys')  
            except Pump.DoesNotExist:
                return redirect('Pump:view_pump_delivery_boys')  
        else:
            return redirect('Pump:view_pump_delivery_boys')  

    return render(request, 'Pump/Add_DeliveryBoy.html')

#////////////////////////////////////////////////////////////////////////////////


def view_pump_delivery_boys(request):
    pump_id = request.session.get('pid')
    if pump_id:
        try:
            pump = Pump.objects.get(pk=pump_id)
            delivery_boys = DeliveryBoy.objects.filter(pumpId=pump)
            return render(request, 'Pump/View_Pump_DeliveryBoys.html', {'delivery_boys': delivery_boys})
        except Pump.DoesNotExist:
            return redirect('Pump:add_deliveryboy')  
    else:
        return redirect('Pump:add_deliveryboy')  

def remove_delivery_boy(request, deliveryboy_id):
    delivery_boy = get_object_or_404(DeliveryBoy, pk=deliveryboy_id)
    delivery_boy.delete()
    return redirect('Pump:view_pump_delivery_boys')

#///////////////////////////////////////////////////////////////////////////////////////////

def view_booking_requests(request):
    current_pump_id = request.session.get('pid') 
    if current_pump_id:
        booking_requests = Booking.objects.filter(pump_id=current_pump_id)
        mechanics = Mechanic.objects.filter(pumpId=current_pump_id)
        delivery_boys = DeliveryBoy.objects.filter(pumpId=current_pump_id)  # Add this line
        return render(request, 'Pump/booking_requests.html', {'booking_requests': booking_requests, 'mechanics': mechanics, 'delivery_boys': delivery_boys})  # Include delivery_boys in the context
    else:
        return render(request, 'Pump/Pump_Home.html')

def accept_booking(request, booking_id):
    booking = Booking.objects.get(id=booking_id)
    booking.status = 'Accepted'
    booking.save()
    return redirect('Pump:view_booking_requests')

def reject_booking(request, booking_id):
    booking = Booking.objects.get(id=booking_id)
    booking.status = 'Rejected'
    booking.save()
    return redirect('Pump:view_booking_requests')


def assign_mechanic(request, booking_id):
    if request.method == 'POST':
        mechanic_id = request.POST.get('mechanic')
        booking = get_object_or_404(Booking, id=booking_id)
        booking.mechanic_id = mechanic_id
        booking.save()
    return redirect('Pump:view_booking_requests')

def assign_delivery_boy(request, booking_id):
    if request.method == 'POST':
        delivery_boy_id = request.POST.get('delivery_boy')
        booking = get_object_or_404(Booking, id=booking_id)
        booking.delivery_boy_id = delivery_boy_id
        booking.save()
    return redirect('Pump:view_booking_requests')


#///////////////////////////////////////////////////////////////

def profile(request):
    pid = request.session.get("pid")
    if pid is None:
        return render(request, "User/Error.html", {"error_message": "User ID not found in session."})
    
    try:
        pump = Pump.objects.get(id=pid)
    except Pump.DoesNotExist:
        return render(request, "User/Error.html", {"error_message": "User does not exist."})
    
    return render(request, "Pump/profile.html", {"pump": pump})



def update_pump_details(request):
    pump_id = request.session.get('pid')
    if pump_id:
        pump = Pump.objects.get(id=pump_id)
        if request.method == 'POST':
            pump.name = request.POST.get('name')
            pump.address = request.POST.get('address')
            pump.phone_number = request.POST.get('phone_number')
            pump.email = request.POST.get('email')
            pump.gst_no = request.POST.get('gst_no')
            pump.save()
            return redirect('Pump:profile')
        return render(request, 'Pump/update_pump_details.html', {'pump': pump})
    else:
       
        pass

def change_pump_password(request):
    pump_id = request.session.get('pid')
    if pump_id:
        pump = Pump.objects.get(id=pump_id)
        if request.method == 'POST':
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')
            if new_password == confirm_password:
                pump.password = new_password
                pump.save()
                return redirect('Pump:profile')
            else:
                error_message = "Passwords do not match."
                return render(request, 'Pump/change_password.html', {'pump': pump, 'error_message': error_message})
        return render(request, 'Pump/change_password.html', {'pump': pump})
    else:
       
        pass

#/////////////////////////////////////////////////////////////////////////


def pump_complaint(request):
    if request.method == 'POST':
        subject = request.POST.get('subject')
        description = request.POST.get('description')

        if 'pid' in request.session:
            pump_id = request.session['pid']
            complaint = PumpComplaint.objects.create(
                pump_id=pump_id,  
                subject=subject,
                description=description,
                created_at=timezone.now()
            )
            return redirect('Pump:Pump_home')
        else:
            return render(request, 'User:Error.html', {'error_message': 'User not logged in.'})
    return render(request, 'Pump/pump_complaint.html')

#///////////////////////////////////////////////////////////////////////////////////////////////////////

def ViewReply(request):
    current_pump_id = request.session.get('pid')
    if current_pump_id:
        pump_complaints = PumpComplaint.objects.filter(pump_id=current_pump_id)
        return render(request, 'Pump/view_repiles.html', {'pump_complaints': pump_complaints})
    else:
        return render(request, 'error.html', {'error_message': 'User not logged in.'})
    
    
    
#/////////////////////////////////////////////////////////////////////////////////////////////////////

def edit_fuel(request, pump_id, fuel_id):
    pump = get_object_or_404(Pump, pk=pump_id)
    fuel = get_object_or_404(Fuel, pk=fuel_id, pumpId=pump)
    
    if request.method == 'POST':
        new_quantity = request.POST.get('quantity')
        if new_quantity:
            try:
                fuel.quantity = new_quantity
                fuel.save()
                messages.success(request, "Fuel quantity updated successfully!")
                return redirect('Pump:view_pump_fuels')
            except Exception as e:
                messages.error(request, f"Failed to update fuel quantity: {str(e)}")
        else:
            messages.error(request, "No quantity provided.")

    return render(request, 'Pump/edit_fuel.html', {'pump': pump, 'fuel': fuel})
    