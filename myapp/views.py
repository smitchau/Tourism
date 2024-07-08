from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
from django.core.mail import send_mail
import random
from django.conf import settings
import razorpay
from django.shortcuts import render,redirect,HttpResponse,get_object_or_404


# Create your views here.
def home(request):
    try:
        user = User.objects.get(email = request.session['email'])
        if user.role == "Tourist":
            users = User.objects.all()
            package = Package.objects.all()
            return render(request,"index.html",{'users':users,'package':package})
        else:
            package = Package.objects.all()
            return render(request,"agent_index.html",{'package':package})
    except:
        users = User.objects.all()
        package = Package.objects.all()
        return render(request,"index.html",{'users':users,'package':package})
    
def signup(request):
    if request.POST:
        print("hello")
        try:
            User.objects.get(email = request.POST['email'])
            messages.error(request, "Email already exists. Please log in.")
            return render(request,"login.html")
        except:
            if request.POST['role'] == "Agent" and int(request.POST['age']) > 20:
                User.objects.create(
                    role = request.POST['role'],
                    name = request.POST['name'],
                    email = request.POST['email'],
                    contact = request.POST['contact'],
                    address = request.POST['address'],
                    password = request.POST['password'],
                )
                
                if request.POST['age']:
                    user = User.objects.get(email = request.POST['email'])
                    user.age = request.POST['age']
                    user.save()
                messages.success(request, "Signup Successful!")
                return render(request,'login.html')
            
            elif request.POST['role'] == "Tourist":
                User.objects.create(
                    role = request.POST['role'],
                    name = request.POST['name'],
                    email = request.POST['email'],
                    contact = request.POST['contact'],
                    address = request.POST['address'],
                    password = request.POST['password'],
                )
                messages.success(request, "Signup Successful!")
                return render(request,'login.html')
            else:
                messages.error(request,"Your age below 20 do not register !!")
                return redirect("index")
                
    else:
        return render(request,"signup.html")
    
def login(request):
    if request.POST:
        try:
            user = User.objects.get(email = request.POST['email'])
            print("===================>tourist",user)

            if user.password == request.POST['password']:
                if user.role == "Tourist":
                    print("===================>tourist")
                    messages.success(request, "Login Successful!")
                    request.session['email']  = request.POST['email']
                    request.session['role']  = user.role
                    request.session['password']  = request.POST['password']
                    return redirect('index')
                else:
                    messages.success(request, "Login Successful!")
                    request.session['email']  = request.POST['email']
                    request.session['role']  = user.role
                    request.session['password']  = request.POST['password']
                    return redirect('agent_index')
            else:
                messages.error(request, "password doesn't match !!")
                return render(request,"login.html")    
        except:
            messages.error(request,"Email id doesn't Register !!")
            return render(request,"login.html")  
    else:
        return render(request,"login.html")   

def logout(request):
    try:
        del request.session['email']
        del request.session['password']
        del request.session['role']
        messages.success(request, "Logout Successful!")
        return redirect("index")
    except:
        package = Package.objects.all()
        return render(request,"index.html",{'package':package})

def forgote_password(request):
    if request.POST:
        try:
            user= User.objects.get(email = request.POST['email'])
            print("user",user)
            request.session['email'] = user.email
            otp = random.randint(1000,9999)
            request.session['otp'] = otp
            print("otp",otp)
            subject = 'OTP For Forgot Password'
            message = 'Hello '+user.name+" , Your OTP : "+str(otp)
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [user.email, ]
            send_mail( subject, message, email_from, recipient_list )
            return render(request,'otp.html')
        except Exception as e:
            messages.error(request,"Email Does Not Exist !!!")
            print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>",e)
            return render(request,'forgote_password.html')
    else:
        return render(request,"forgote_password.html")

def otp(request):
    if request.POST:
        uotp = int(request.POST['otp'])
        print("uotp",type(uotp))
        print(request.session['otp'],type(request.session['otp']))
        
        if uotp == request.session['otp']:
            return render(request,'newpassword.html')
        else:
            msg="Invalid OTP"
            return render(request,'otp.html',{'msg':msg})        
    else:
        return render(request,"otp.html")

def newpassword(request):
    if request.POST:
        np = request.POST['password']
    
        user=User.objects.get(email = request.session['email'])
        user.password=np
        user.save()
        del request.session['email']
        del request.session['otp']
        msg1="Password Updated :) "
        return render(request, 'login.html',{'msg1':msg1})       
    else:
        return render(request,"newpassword.html")

    
def profile_page(request):
    user = User.objects.get(email = request.session['email'])
    print(user)
    return render(request,"profile_page.html",{'user':user})

def change_image(request):
    try:
        user = User.objects.get(email = request.session['email'])
        print(user)
        if request.POST:
            user.profile_image = request.FILES.get('profile_image')
            user.save()
            return render(request,"profile_page.html",{'user':user})
        else:
            return render(request,"profile_page.html",{'user':user})
    except Exception as e:
        print(e)
        return redirect("index")

def update_profile(request):
    try:
        user = User.objects.get(email = request.session['email'])
        print(user)
        if request.POST:
            user.name = request.POST['name']
            user.email = request.POST['email']
            user.contact = request.POST['contact']
            user.address = request.POST['address']
            user.age = request.POST['age']
            user.disignation = request.POST['designation']
            user.facebooklink = request.POST['facebooklink']
            user.instagram = request.POST['instagram']
            user.twiter = request.POST['twitter']
            user.save()
            messages.success(request,"Profile Updated")
            return render(request,"profile_page.html",{'user':user})
        else:    
            return render(request,"update_profile.html",{'user':user})
    except Exception as e:
        print(e)
        return redirect("index")

def change_password(request):
    if request.POST:
        try:
            user = User.objects.get(email = request.session['email'])
            print("========>",user)
            
            if user.password == request.POST['password']:
                if request.POST['npassword'] == request.POST['cpassword']:
                    user.password = request.POST['npassword']
                    user.save()
                    messages.success(request,'password successfully changed')
                    del request.session['email']
                    del request.session['password']
                    return redirect('login')
                else:
                    messages.error(request,"New password and Confirm password doesn't match !!")
                    return render(request,'change_password.html')

            else:
                messages.error(request,"current password doesn't match !!")
                return render(request,'change_password.html')

        except:
            messages.error(request,"please enter currect Email id !!")
            return render(request,'change_password.html')

    else:
        return render(request,'change_password.html')


def about(request):
    try:
        user = User.objects.all()
        return render(request,"about.html",{'user':user})
    except Exception as e:
        print(e)
        return redirect("index")
        
def service(request):
    return render(request,"service.html")

def package(request):
    try:
        package = Package.objects.all()
        return render(request,"package.html",{'package':package})
    except Exception as e:
        print(e)
        messages.error(request,"Email not register")
        return render(request,"package.html")

def destination(request):
    return render(request,"destination.html")

def booking(request):
    try:
        if request.method == 'POST':
            if int(request.POST['age']) > 15:
                user = User.objects.get(email = request.session['email'])
                selected_package_info = request.POST['packagename'].split('|')
                selected_package_id = selected_package_info[0]
                selected_price = float(selected_package_info[1])
                username = request.POST['username']
                age = int(request.POST['age'])
                contact = int(request.POST['contact'])
                address = request.POST['address']
                package = Package.objects.get(pk = selected_package_id)
                print(package)
                if package.Available_slot > 0:
                    package.Available_slot = package.Available_slot - 1
                    package.save()
                    # Create Booking object with current date
                    booking = Booking.objects.create(
                        user = user,
                        package_id=selected_package_id,
                        packagename=Package.objects.get(pk=selected_package_id).packagename,
                        packageprice=selected_price,
                        username=username,
                        age=age,
                        contact=contact,
                        address=address,
                    )
                    
                    print("=================================")
    
                    client = razorpay.Client(auth = (settings.RAZORPAY_KEY_ID,settings.RAZORPAY_KEY_SECRET))
                    payment = client.order.create({'amount': booking.packageprice * 100, 'currency': 'INR', 'payment_capture': 1})
                    booking.razorpay_order_id = payment['id']  
                    booking.save()

                    request.session['name']= booking.packagename
                    print(request.session['name'])

                    context = {
                            'payment': payment,
                            'booking':booking,  # Ensure the amount is in paise
                        }
                    
                    print("=======================",context)
                    print("&7777777777777777777777",payment)


                    
                    return render(request, 'payments.html',context)
                
                else:
                    messages.error(request,"Sorry Slot is Full !!")
                    return redirect("index")
            else:
                messages.error(request,"Sorry your age is not valid !!")
                return redirect("index")

        package = Package.objects.all()
        return render(request, "booking.html", {'package': package})
    
    except Exception as e:
        messages.error(request,"e")
        return redirect("index")  # Redirect to logout page if user does not exist or session is invalid
   
def payments(request):
    return render(request,"payments.html") 

def success(request):
    try:
            user = User.objects.get(email = request.session['email'])
            booking = Booking.objects.filter(user=user).latest('razorpay_order_id')
            print("success",booking)
            razorpay_payment_id = request.GET.get('razorpay_payment_id')
            print("=============",razorpay_payment_id)
            if razorpay_payment_id != "":
                # Update the booking instance with the Razorpay payment ID
                booking.razorpay_payment_id = razorpay_payment_id
                booking.save()
                try:
                    subject = 'Tourist'
                    message = 'Hello '+user.name+" , Your Package Booking Successfull... " + " , Have a Nice Day"
                    email_from = settings.EMAIL_HOST_USER
                    recipient_list = [user.email, ]
                    send_mail( subject, message, email_from, recipient_list )
                    print("Done",booking)
                    return render(request,'success.html')
                except:
                    print("Done",booking)
                    return render(request,'success.html')
            else:
                msg= "Please Book Ride Again Payment are not store....."
                messages.info(request,msg)
                booking.delete()
                return render(request,"index.html")
    except:
        return render(request,"index.html")

    
def yourbooking(request):
    try:
        user = User.objects.get(email = request.session['email'])
        print(user)
        booking = Booking.objects.filter(user = user)
        print(booking)
        return render(request,"yourbooking.html",{'booking':booking})        
    except Exception as e:
        print(e)
        return render(request,"yourbooking.html")
    
def delbooking(request,pk):
    booking = Booking.objects.get(pk = pk)
    package = Package.objects.get(pk = booking.package.pk)
    print(package)
    package.Available_slot += 1
    package.save()
    booking.delete()
    messages.success(request,"Booking successfully deleted")
    return redirect("index")
    
def team(request):
    users = User.objects.all()
    return render(request,"team.html",{'users':users})

def testimonial(request):
    return render(request,"testimonial.html")

def contact(request):
    if request.POST:
        Contact.objects.create(
            name = request.POST['name'],
            email = request.POST['email'],
            subject = request.POST['subject'],
            message = request.POST['message']
        )
        messages.success(request,"message successfully send")
        return redirect("contact")
    else:    
        return render(request,"contact.html")

def slot_member(request,pk):
    try:
        booking = Booking.objects.filter(package = pk)
        return render(request,"slot_member.html",{'booking':booking})
    except Exception as e:
        print("==========",e)
        return render(request,"slot_member.html")

#========================================Agent view==================================

def agent_index(request):
    try:
        user = User.objects.get(email = request.session['email'])
        package = Package.objects.all()
        return render(request,"agent_index.html",{'package':package})
    except Exception as e:
        print(e)
        return render(request,"agent_index.html")


def agent_service(request):
    return render(request,"agent_service.html")

def agent_contact(request):
    return render(request,"agent_contact.html")

def add_package(request):
    try:
        user = User.objects.get(email=request.session['email'])  # Retrieve user based on session email
        if user.role == "Agent":
            if request.method == 'POST':
                # Create Package object
                package = Package.objects.create(
                    user = user,
                    packagename=request.POST.get('packagename'),
                    placename=request.POST.get('placename'),
                    movefrom=request.POST.get('movefrom'),
                    tofrom=request.POST.get('tofrom'),
                    movedate=request.POST.get('movedate'),
                    todate=request.POST.get('todate'),
                    price=request.POST.get('price'),
                    totaltourist=request.POST.get('totaltourist'), 
                    Available_slot = request.POST.get('totaltourist'),
                    image=request.FILES.get('image')  # Use get() method to retrieve file field
                )
                
                print("Package created successfully:", package)

                # Get day descriptions
                day_descriptions = request.POST.getlist('day_description[]')

                # Save day descriptions for the package
                for i, description in enumerate(day_descriptions, start=1):
                    DayDescription.objects.create(
                        package=package,
                        day_number=i,
                        description=description
                    )
                messages.success(request,"Package created successfully:")
                # Redirect to a success page or render another template after successful form submission
                return render(request, "add_images.html",{'package':package})
            else:
                #   Render the form for GET request
                return render(request, "add_package.html")
    
    except User.DoesNotExist:
        print("User does not exist")
        return redirect('logout')  # Redirect to logout page if user does not exist or session is invalid
    
    except Exception as e:
        print("Exception occurred:", str(e))
        return redirect('logout')  # Redirect to logout page for any other exceptions or errors

def add_images(request,pk):
        print("hii")
        user = User.objects.get(email=request.session['email'])  # Retrieve user based on session email
        print(user)
        package = Package.objects.get(pk = pk)
        print(package)
        if user.role == "Agent":
            if request.POST:
                print("hello")
                num_images = int(request.POST.get('num_images'))
                for i in range(1, num_images + 1):
                    image_file = request.FILES.get(f'image_{i}')
                    PackageImage.objects.create(
                        package=package,
                        image=image_file
                    )
                return redirect("index")
            else:
                return render(request,"add_images.html")

   
def view_all_package(request):
    try:
        user = User.objects.get(email = request.session['email'])
        package = Package.objects.all()
        return render(request,"view_all_package.html",{'package':package,'user':user})
    except Exception as e:
        print(e)
        return render(request,"view_all_package.html")
    
def view_your_package(request):
    try:
        user = User.objects.get(email = request.session['email'])
        print(user)
        package = Package.objects.filter(user = user)
        print(package)
        
        if user.role == "Agent":
            return render(request,"view_your_package.html",{'package':package})
    except Exception as e:
        print(e)
        return render(request,'index.html')

def package_detail(request,pk):
    try:
        user = User.objects.get(email = request.session['email'])
        print("user",user)
        
        package = Package.objects.get(pk = pk)
        print(package,pk)
        print("==========package.user",package.user)
        daydisc = DayDescription.objects.filter(package = pk)
        print(daydisc)
        images = PackageImage.objects.filter(package = pk)
        print(images)
        count = 0
        for i in daydisc:
            count += 1
        print(count)
        return render(request,"package_detail.html",{'user':user,'package':package,'daydisc':daydisc,'images':images,'count':count})
        
    except Exception as e:
        print("Exception",e)
        package = Package.objects.get(pk = pk)
        print(package,pk)
        daydisc = DayDescription.objects.filter(package = pk)
        print(daydisc)
        images = PackageImage.objects.filter(package = pk)
        print(images)
        count = 0
        for i in daydisc:
            count += 1
        print(count)
        return render(request,"package_detail.html",{'package':package,'daydisc':daydisc,'images':images,'count':count})
       
def delete_package(request,pk):
    user = User.objects.get(email = request.session['email'])
    print(user)
    try:
        package = Package.objects.get(pk = pk)
        package.delete()
        package = Package.objects.filter(user = user)
        print(package)
        messages.success(request,"Package deleted")
        return redirect("view_your_package")   
    except:
        package = Package.objects.get(pk = pk)
        print(package,pk)
        daydisc = DayDescription.objects.filter(package = pk)
        print(daydisc)
        images = PackageImage.objects.filter(package = pk)
        print(images)
        count = 0
        for i in daydisc:
            count += 1
        print(count)
        return render(request,"package_detail.html",{'package':package,'daydisc':daydisc,'images':images,'count':count})


def update_package(request,pk):
    user = User.objects.get(email = request.session['email'])
    try:
        if request.POST:
            package = Package.objects.get(pk = pk)
            daydisc = DayDescription.objects.filter(package = package)
            package.packagename = request.POST['packagename']
            package.placename = request.POST['placename']
            package.movefrom = request.POST['movefrom']
            package.tofrom = request.POST['tofrom']
            package.price = request.POST['price']
            package.totaltourist = request.POST['totaltourist']
            package.save()
            day_descriptions = request.POST.getlist('day_description[]')

            for i, day in enumerate(daydisc):
                    description = request.POST.get(f'day_description_{day.id}', '')
                    day.description = description
                    day.save()
             
            package = Package.objects.filter(user = user)
            
            messages.success(request,"Package Updated")
            return redirect("view_your_package")  
        else:
            package = Package.objects.get(pk = pk)
            
            print("package == ",package)
            
            daydisc = DayDescription.objects.filter(package = package)
            print(daydisc)
            images = PackageImage.objects.filter(package = package)
            print(images)
            count = 0
            for i in daydisc:
                count += 1
            print(count)
            return render(request,"update_package.html",{'package':package,'daydisc':daydisc,'images':images,'count':count})
            
    except Exception as e:
        print(e)
        return redirect("index")