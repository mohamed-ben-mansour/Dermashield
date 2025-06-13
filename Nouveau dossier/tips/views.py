from django.shortcuts import render, get_object_or_404, redirect
from .models import Tip
from .forms import TipForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .forms import TipForm

@login_required(login_url='login')
def admin_only_view(request):
    if not request.user.is_staff:
        return HttpResponseForbidden("You do not have permission to view this page.")

    if request.method == "POST":
        form = TipForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('main_page')  # Redirect to a success page
    else:
        form = TipForm()

    return render(request, "tip_form.html", {'form': form})

def main_page(request):
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



def tip_update(request, pk):
    tip = get_object_or_404(Tip, pk=pk)
    form = TipForm(request.POST or None, instance=tip)
    if form.is_valid():
        form.save()
        return redirect('main_page')  
    return render(request, 'tip_form.html', {'form': form})

def tip_delete(request, pk):
    tip = get_object_or_404(Tip, pk=pk)
    if request.method == 'POST':
        tip.delete()
        return redirect('main_page')  
    return render(request, 'tip_confirm_delete.html', {'tip': tip})