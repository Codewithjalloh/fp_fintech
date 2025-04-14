from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Property, PropertyDocument

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(max_length=15, required=True)
    national_id = forms.CharField(max_length=20, required=True)
    date_of_birth = forms.DateField(required=True)
    address = forms.CharField(widget=forms.Textarea, required=True)
    employment_status = forms.CharField(max_length=50, required=True)
    monthly_income = forms.DecimalField(max_digits=10, decimal_places=2, required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'first_name', 'last_name',
                  'phone_number', 'national_id', 'date_of_birth', 'address',
                  'employment_status', 'monthly_income')

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'phone_number', 'address',
                  'employment_status', 'monthly_income')

class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = ('property_type', 'location', 'size', 'estimated_value', 'description')

class PropertyDocumentForm(forms.ModelForm):
    class Meta:
        model = PropertyDocument
        fields = ('document_type', 'document_file') 