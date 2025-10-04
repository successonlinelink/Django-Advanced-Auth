from django.shortcuts import redirect, render
from authuser.forms import UserRegisterForm 
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from authuser.models import User

# Email Verification Imports
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
# End of Email Verification Imports


def register_view(request):
    if request.user.is_authenticated:
        messages.warning(request, f"Hey you are already Logged In.")
        return redirect("core:home")
    
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            # Save the user but mark inactive until email verified
            new_user = form.save(commit=False)
            new_user.is_active = False
            new_user.save()

            # Email verification
            current_site = get_current_site(request)
            mail_subject = "Activate your account."
            message = render_to_string("accounts/acc_active_email.html", {
                "user": new_user,
                "domain": current_site.domain,
                "uid": urlsafe_base64_encode(force_bytes(new_user.pk)),
                "token": default_token_generator.make_token(new_user),
            })

            to_email = form.cleaned_data["email"]
            email_msg = EmailMessage(mail_subject, message, to=[to_email])
            email_msg.send()

            messages.success(request, "Please confirm your email address to complete the registration.")
            return redirect("/authuser/login/?command=verification&email=" + to_email)
        
        # else:
        #     messages.error(request, "Error creating account, please try again.")
            
    else:
        form = UserRegisterForm()

    context = { 'form': form }
    return render(request, "authuser/register.html", context)

# Activate Email
def activate(request, uidb64, token):
    
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    
    except(TypeError, OverflowError, ValueError, User.DoesNotExist):
        user = None

    # Check the token
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()

        messages.success(request, 'Your account has been created')
        return redirect('authuser:login')

    else:
        messages.error(request, "Invalid activation link")
        return redirect('authuser:login')
    

# Login
def login_view(request):
    if request.user.is_authenticated:
        messages.warning(request, f"Hey you are already Logged In.")
        return redirect("core:home")
    
    if request.method == "POST":
        email = request.POST.get("email")  
        password = request.POST.get("password")   

        try:
            user = User.objects.get(email=email)
            user = authenticate(request, email=email, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, "You are logged in.")
                return redirect("core:home")
            else:
                messages.warning(request, "User Does Not Exist, create an account.")
    
        except:
            messages.warning(request, f"User with {email} does not exist")
    
    return render(request, "authuser/login.html")

# Log Out
def logout_view(request):
    logout(request)
    messages.success(request, "You logged out.")
    return redirect("authuser:login")

# Forget Password
def forget_password(request):
    
    if request.method == "POST":
        email = request.POST.get("email")

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email__exact=email)

            # Email verification
            current_site = get_current_site(request)
            mail_subject = "Reset your password."
            message = render_to_string("authuser/reset_password_email.html", {
                "user": user,
                "domain": current_site,
                "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                "token": default_token_generator.make_token(user),
            })

            to_email = email
            email_msg = EmailMessage(mail_subject, message, to=[to_email])
            email_msg.send()

            messages.success(request, "Password reset link has been sent to your email address.")
            return redirect("authuser:login")

        else:
            messages.error(request, f"Account with {email} does not exist.")
    return render(request, "authuser/forget_password.html")


# Reset Validate
def reset_validate(request, uidb64, token):
    
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    
    except(TypeError, OverflowError, ValueError, User.DoesNotExist):
        user = None

    # Check the token
    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request, 'Please reset your password')
        return redirect('authuser:reset_password')

    else:
        messages.error(request, "This link has been expired!")
        return redirect('authuser:login')


# Reset Password
def reset_password(request):
    if request.method == "POST":
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password == confirm_password:
            uid = request.session.get('uid') # Get uid from session cos it has been stored there in reset_validate view
            user = User.objects.get(pk=uid) # Get user by primary key
            user.set_password(password)
            user.save()
            messages.success(request, "Password reset successful.")
            return redirect("authuser:login")
        
        else:
            messages.error(request, "Password do not match!")
            return redirect("authuser:reset_password")
    
    return render(request, "authuser/reset_password.html")