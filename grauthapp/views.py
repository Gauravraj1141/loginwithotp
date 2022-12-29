from django.shortcuts import render, redirect
from .sender import send_otp_to_phone
from .models import CustomUser
from django.contrib.auth import login, authenticate, logout


def home(request):
    return render(request, "grsolapp/home.html")


def User_register(request):
    if request.method == "POST":
        print("in register", request.user.is_authenticated)
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        Password = request.POST.get("Password")
        username = request.POST.get("username")

        check_email = CustomUser.objects.filter(email=email).first()
        check_phone = CustomUser.objects.filter(Phone_number=phone).first()
        if check_email or check_phone:
            if check_email:
                msg = "Email is Already registered"
            elif check_phone:
                msg = "This Phone Number is Already registered"
            context = {"message": msg,
                       "class": "danger"}
            return render(request, "grsolapp/register.html", context)
        else:
            user_data = CustomUser.objects.create(
                username=username, email=email, Phone_number=phone)
            user_data.set_password(Password)
            user_data.save()
            request.session["mobile"] = phone
            return redirect("login")

    return render(request, "grsolapp/register.html")

# login form


def User_login(request):

    print("in login", request.user.is_authenticated)

    if request.method == "POST":
        phone = request.POST.get("phone")
        registered_phone = request.session["mobile"]

        if phone == registered_phone:
            otp = send_otp_to_phone(registered_phone)
            CustomUser.objects.filter(Phone_number=phone).update(
                otp=otp, Phone_is_verified=True)
            request.session["otp"] = otp
            print(otp)
            return redirect("enterOtp")
    return render(request, "grsolapp/login.html")


def Enter_otp(request):
    context = {"message": "we have sent an otp to your registered mobile number",
               "class": "success", "phone": request.session["mobile"]}
    if request.method == "POST":

        enterotp = request.POST.get("otp")
        otp = request.session['otp']

        if str(enterotp) == str(otp):
            user = authenticate(request=request, otp=enterotp)
            login(request, user)
            return redirect("profile")
        else:
            context = {"message": "invalid otp ",
                       "class": "warning"}

            return render(request, "grsolapp/otp.html", context)

    return render(request, "grsolapp/otp.html", context)


def User_profile(request):
    print("in profile", request.user.is_authenticated)
    context = {"message": "welcome to your profile",
               "class": "success"}
    return render(request, "grsolapp/profile.html", context)


def User_logout(request):
    logout(request)
    return redirect("login")
