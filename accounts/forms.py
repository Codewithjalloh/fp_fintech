from django import forms
from django.contrib.auth.forms import UserCreationForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Field
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
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('property_type', css_class='form-group col-md-6 mb-0'),
                Column('location', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('size', css_class='form-group col-md-6 mb-0'),
                Column('estimated_value', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            'description',
            Submit('submit', 'Save Property', css_class='btn btn-primary w-100 mt-3')
        )
        
        # Add placeholders and help text
        self.fields['property_type'].widget.attrs.update({'class': 'form-select'})
        self.fields['location'].widget.attrs.update({'placeholder': 'Enter property location'})
        self.fields['size'].widget.attrs.update({'placeholder': 'Enter size in square meters'})
        self.fields['estimated_value'].widget.attrs.update({'placeholder': 'Enter estimated value'})
        self.fields['description'].widget.attrs.update({
            'placeholder': 'Enter property description',
            'rows': 4
        })

    class Meta:
        model = Property
        fields = ('property_type', 'location', 'size', 'estimated_value', 'description')
        labels = {
            'property_type': 'Property Type',
            'location': 'Location',
            'size': 'Size (m²)',
            'estimated_value': 'Estimated Value',
            'description': 'Description'
        }

class PropertyDocumentForm(forms.ModelForm):
    class Meta:
        model = PropertyDocument
        fields = ('document_type', 'document_file') 