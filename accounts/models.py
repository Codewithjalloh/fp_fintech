from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator

class User(AbstractUser):
    phone_number = models.CharField(max_length=15, unique=True, null=True, blank=True)
    national_id = models.CharField(max_length=20, unique=True, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    employment_status = models.CharField(max_length=50, null=True, blank=True)
    monthly_income = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(0)], null=True, blank=True)
    
    def __str__(self):
        return f"{self.get_full_name()} ({self.username})"

class PropertyDocument(models.Model):
    DOCUMENT_TYPES = [
        ('land_title', 'Land Title'),
        ('lease_agreement', 'Lease Agreement'),
        ('building_permit', 'Building Permit'),
        ('property_valuation', 'Property Valuation'),
        ('other', 'Other'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='property_documents')
    document_type = models.CharField(max_length=50, choices=DOCUMENT_TYPES)
    document_file = models.FileField(upload_to='property_documents/')
    upload_date = models.DateTimeField(auto_now_add=True)
    verified = models.BooleanField(default=False)
    verification_notes = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.get_document_type_display()}"

class Property(models.Model):
    PROPERTY_TYPES = [
        ('land', 'Land'),
        ('residential', 'Residential Building'),
        ('commercial', 'Commercial Building'),
        ('mixed_use', 'Mixed Use'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('verified', 'Verified'),
        ('rejected', 'Rejected'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='properties')
    property_type = models.CharField(max_length=50, choices=PROPERTY_TYPES)
    location = models.CharField(max_length=255)
    size = models.DecimalField(max_digits=10, decimal_places=2, help_text="Size in square meters")
    estimated_value = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(0)])
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.get_property_type_display()} at {self.location}"

class UserDocument(models.Model):
    DOCUMENT_TYPES = [
        ('national_id', 'National ID'),
        ('passport', 'Passport'),
        ('employment_letter', 'Employment Letter'),
        ('bank_statement', 'Bank Statement'),
        ('tax_clearance', 'Tax Clearance'),
        ('other', 'Other'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='documents')
    document_type = models.CharField(max_length=50, choices=DOCUMENT_TYPES)
    document_file = models.FileField(upload_to='user_documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_document_type_display()} for {self.user}"
