from django.shortcuts import render, redirect, get_object_or_404
from .forms import RegisterForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from .models import Prescriptions


@login_required(login_url="/login")
def home(request):
    return render(request, 'main/home.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/home')
        else:
            return render(request, 'registration/login.html', {'error': 'Invalid username or password.'})
    else:
        return render(request, 'registration/login.html')


def sign_up(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/home')
    else:
        form = RegisterForm()

    return render(request, 'registration/sign_up.html', {"form": form})


@login_required
def edit_prescription(request, prescription_id):
    prescription = get_object_or_404(Prescriptions, id=prescription_id)
    if request.method == 'POST':
        prescription.medication_name = request.POST['medication_name']
        prescription.dosage = request.POST['dosage']
        prescription.instructions = request.POST['instructions']
        prescription.start_date = request.POST['start_date']
        prescription.end_date = request.POST['end_date']
        prescription.save()
        return redirect('prescription_detail', prescription.id)
    return render(request, 'main/Prescriptions.html', {'prescription': prescription})