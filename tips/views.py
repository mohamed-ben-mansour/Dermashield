from django.shortcuts import render, get_object_or_404, redirect
from .models import Tip
from .forms import TipForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseForbidden

# Custom check for admin users
def user_is_admin(user):
    return user.is_staff

@login_required(login_url='login')  # Redirect to login if the user is not authenticated
def admin_only_view(request):
    # Check if the user is a staff member, if not, deny access
    if not request.user.is_staff:
        return HttpResponseForbidden("You do not have permission to view this page.")

    # Handling POST request (form submission)
    if request.method == "POST":
        form = TipForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()  # Save the new tip
            return redirect('main_page')  # Redirect to the main page or any other success page after form submission
    else:
        form = TipForm()  # Empty form for GET request
    
    return render(request, "tip_form.html", {'form': form})  # Render the form to the template

def main_page(request):
    # Fetching tips by categories
    protection_tips = Tip.objects.filter(category='protection')
    treatment_tips = Tip.objects.filter(category='treatment')
    
    # Add a variable to check if the user is staff (admin)
    is_admin = request.user.is_staff

    context = {
        'protection_tips': protection_tips,
        'treatment_tips': treatment_tips,
        'is_admin': is_admin,  # Add this to the context
    }
    return render(request, 'index.html', context)

def tip_detail(request, tip_id):
    tip = get_object_or_404(Tip, id=tip_id)
    is_admin = request.user.is_staff  # Check if the user is an admin
    return render(request, 'detail.html', {'tip': tip, 'is_admin': is_admin})

@login_required
@user_passes_test(user_is_admin)
def tip_update(request, pk):
    tip = get_object_or_404(Tip, pk=pk)  # Get the existing tip by ID
    if request.method == "POST":
        form = TipForm(request.POST, request.FILES, instance=tip)  # Bind form to the existing instance
        if form.is_valid():
            form.save()  # Save the changes to the existing tip, not create a new one
            return redirect('main_page')  # Redirect to the main page after the update
    else:
        form = TipForm(instance=tip)  # Empty form for GET request with the current tip data

    return render(request, 'tip_form.html', {'form': form})


@login_required
@user_passes_test(user_is_admin)
def tip_delete(request, pk):
    tip = get_object_or_404(Tip, pk=pk)
    if request.method == 'POST':
        tip.delete()
        return redirect('main_page')  
    return render(request, 'tip_confirm_delete.html', {'tip': tip})
