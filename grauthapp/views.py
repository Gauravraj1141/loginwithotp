from django.shortcuts import render, redirect, HttpResponse
from .sender import send_otp_to_phone
from .models import CustomUser
from django.contrib.auth import login, authenticate, logout
from .forms import OTPForm
from .authbackend import OTPAuthBackend


def home(request):
    if request.user.is_authenticated:
        ulogin = True
    else:
        ulogin = False
    context = {"login": ulogin}
    return render(request, "grsolapp/home.html", context)


def User_register(request):
    if not request.user.is_authenticated:
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
                    msg = "Phone Number is Already registered"
                context = {"message": msg,
                           "class": "danger"}
                return render(request, "grsolapp/register.html", context)
            else:
                user_data = CustomUser.objects.create(
                    username=username, email=email, Phone_number=phone)
                user_data.set_password(Password)
                user_data.save()
                request.session["mobile"] = phone
                return redirect("/login/")

        return render(request, "grsolapp/register.html")
    else:
        return redirect("/profile/")


# login form


def User_login(request):
    if not request.user.is_authenticated:
        print("in login", request.user.is_authenticated)

        if request.method == "POST":
            print("it is post req by user login")
            phone = request.POST.get("phone")

            try:
                registered_phone = request.session['mobile']
            except Exception as e:
                registered_phone = CustomUser.objects.get(
                    Phone_number=phone).Phone_number
            print(registered_phone)

            if phone == registered_phone:
                otp = send_otp_to_phone(registered_phone)
                CustomUser.objects.filter(Phone_number=phone).update(
                    otp=otp, Phone_is_verified=True)
                request.session["otp"] = otp
                print(otp)
                return redirect("/enterOtp/")
            else:
                return HttpResponse("hey session is not avaialable")
        else:
            return render(request, "grsolapp/login.html")

    else:
        return redirect("/profile/")


def Enter_otp(request):
    print("in otp", request.user.is_authenticated)

    if not request.user.is_authenticated:
        if request.method == "POST":
            formdata = OTPForm(request.POST)
            if formdata.is_valid():
                otp = formdata.cleaned_data['otp']
                print("otp is ========", otp)
                user = authenticate(request=request, otp=otp)
                print(user)
                if user is not None:
                    login(request, user)
                    print(user)
                    return redirect("/profile/")
                else:
                    print("hey user is non")

            else:
                context = {"message": "invalid otp ",
                           "class": "warning"}

                return render(request, "grsolapp/otp.html", context)
        formdata = OTPForm()
        return render(request, "grsolapp/otp.html", {"form": formdata})

    else:
        return redirect("/profile/")


def User_profile(request):
    if request.user.is_authenticated:
        print("in profile", request.user.is_authenticated)
        context = {"message": "welcome to your profile",
                   "class": "success"}
        return render(request, "grsolapp/profile.html", context)
    else:
        return redirect("/login/")


def User_logout(request):
    logout(request)
    return redirect("/login/")
