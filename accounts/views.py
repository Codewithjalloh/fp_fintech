from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegistrationForm, UserProfileForm, PropertyForm, PropertyDocumentForm
from .models import User, Property, PropertyDocument

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('accounts:dashboard')
    else:
        form = UserRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful!')
            return redirect('accounts:dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'accounts/login.html')

def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('core:home')

@login_required
def profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('accounts:profile')
    else:
        form = UserProfileForm(instance=request.user)
    return render(request, 'accounts/profile.html', {'form': form})

@login_required
def dashboard(request):
    user = request.user
    properties = Property.objects.filter(user=user)
    loan_applications = user.loan_applications.all()
    documents = PropertyDocument.objects.filter(user=user)
    
    context = {
        'properties': properties,
        'loan_applications': loan_applications,
        'documents': documents,
    }
    return render(request, 'accounts/dashboard.html', context)

@login_required
def add_property(request):
    if request.method == 'POST':
        form = PropertyForm(request.POST)
        if form.is_valid():
            property = form.save(commit=False)
            property.user = request.user
            property.save()
            messages.success(request, 'Property added successfully!')
            return redirect('accounts:dashboard')
    else:
        form = PropertyForm()
    return render(request, 'accounts/property_form.html', {'form': form, 'title': 'Add Property'})

@login_required
def property_detail(request, property_id):
    property = get_object_or_404(Property, id=property_id, user=request.user)
    return render(request, 'accounts/property_detail.html', {'property': property})

@login_required
def edit_property(request, property_id):
    property = get_object_or_404(Property, id=property_id, user=request.user)
    if request.method == 'POST':
        form = PropertyForm(request.POST, instance=property)
        if form.is_valid():
            form.save()
            messages.success(request, 'Property updated successfully!')
            return redirect('accounts:property_detail', property_id=property.id)
    else:
        form = PropertyForm(instance=property)
    return render(request, 'accounts/property_form.html', {'form': form, 'title': 'Edit Property'})

@login_required
def delete_property(request, property_id):
    property = get_object_or_404(Property, id=property_id, user=request.user)
    if request.method == 'POST':
        property.delete()
        messages.success(request, 'Property deleted successfully!')
        return redirect('accounts:dashboard')
    return render(request, 'accounts/property_confirm_delete.html', {'property': property})

@login_required
def upload_document(request):
    if request.method == 'POST':
        form = PropertyDocumentForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            document.user = request.user
            document.save()
            messages.success(request, 'Document uploaded successfully!')
            return redirect('accounts:dashboard')
    else:
        form = PropertyDocumentForm()
    return render(request, 'accounts/document_form.html', {'form': form})

@login_required
def delete_document(request, document_id):
    document = get_object_or_404(PropertyDocument, id=document_id, user=request.user)
    if request.method == 'POST':
        document.delete()
        messages.success(request, 'Document deleted successfully!')
        return redirect('accounts:dashboard')
    return render(request, 'accounts/document_confirm_delete.html', {'document': document})
