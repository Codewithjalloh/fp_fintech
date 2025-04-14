from django.db import models
from accounts.models import User, Property
from django.core.validators import MinValueValidator

class LoanApplication(models.Model):
    LOAN_PURPOSES = [
        ('land_purchase', 'Land Purchase'),
        ('construction', 'Construction'),
        ('renovation', 'Renovation'),
        ('property_improvement', 'Property Improvement'),
        ('other', 'Other'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('under_review', 'Under Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('disbursed', 'Disbursed'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='loan_applications')
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='loan_applications')
    loan_purpose = models.CharField(max_length=50, choices=LOAN_PURPOSES)
    amount_requested = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(0)])
    repayment_period = models.IntegerField(help_text="Repayment period in months")
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    application_date = models.DateTimeField(auto_now_add=True)
    review_date = models.DateTimeField(null=True, blank=True)
    approval_date = models.DateTimeField(null=True, blank=True)
    disbursement_date = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True)
    
    def __str__(self):
        return f"Loan Application #{self.id} - {self.user.get_full_name()}"

class LoanDisbursement(models.Model):
    loan_application = models.OneToOneField(LoanApplication, on_delete=models.CASCADE, related_name='disbursement')
    disbursement_amount = models.DecimalField(max_digits=15, decimal_places=2)
    disbursement_date = models.DateTimeField(auto_now_add=True)
    mobile_money_transaction_id = models.CharField(max_length=100)
    disbursement_method = models.CharField(max_length=50)
    notes = models.TextField(blank=True)
    
    def __str__(self):
        return f"Disbursement for Loan #{self.loan_application.id}"

class Repayment(models.Model):
    loan_application = models.ForeignKey(LoanApplication, on_delete=models.CASCADE, related_name='repayments')
    amount_paid = models.DecimalField(max_digits=15, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    mobile_money_transaction_id = models.CharField(max_length=100)
    payment_method = models.CharField(max_length=50)
    is_late = models.BooleanField(default=False)
    late_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    notes = models.TextField(blank=True)
    
    def __str__(self):
        return f"Repayment for Loan #{self.loan_application.id} - {self.payment_date}"
