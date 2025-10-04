from django.shortcuts import render, redirect
from authuser import models as user_models
from authuser.models import Profile
from accounts.forms import UpdateProfileForm
from django.contrib import messages
from django.contrib.auth.hashers import check_password

def dashboard(request):
    context = {}
    return render(request, 'accounts/dashboard.html', context)

# # Update Profile
def update_profile(request):
    profile = Profile.objects.get(user=request.user)
    if request.method == 'POST':
        form = UpdateProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.user = request.user
            new_form.save()
            
            messages.success(request, "Profile Updated Successfully.")
            return redirect("accounts:update_profile")
        
    else:
        form = UpdateProfileForm(instance=profile)
    
    context = {'profile': profile, "form": form}
    return render(request, 'accounts/update_profile.html', context)

# # change Password
def change_password(request):
    if request.method == 'POST':
        old_password = request.POST.get("old_password")
        new_password = request.POST.get("new_password")
        confirm_new_password = request.POST.get("confirm_new_password")

        if confirm_new_password != new_password:
            messages.error(request, "Confirm Password and New Password does not Match!")
            return redirect("accounts:change_password")

        if check_password(old_password, request.user.password):
            request.user.set_password(new_password)
            request.user.save()

            messages.success(request, "Password Changed Successfully!")
            return redirect("accounts:change_password")
        
        else:
            messages.error(request, "Old Password is not correct")
            return redirect("accounts:change_password")

    context = {}
    return render(request, 'accounts/change_password.html', context)