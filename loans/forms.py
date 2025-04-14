from django import forms
from .models import LoanApplication, LoanDisbursement, Repayment

class LoanApplicationForm(forms.ModelForm):
    class Meta:
        model = LoanApplication
        fields = ('property', 'loan_purpose', 'amount_requested', 'repayment_period', 'interest_rate', 'notes')

class LoanDisbursementForm(forms.ModelForm):
    class Meta:
        model = LoanDisbursement
        fields = ('loan_application', 'disbursement_amount', 'disbursement_method', 'mobile_money_transaction_id', 'notes')

class RepaymentForm(forms.ModelForm):
    class Meta:
        model = Repayment
        fields = ('loan_application', 'amount_paid', 'payment_method', 'mobile_money_transaction_id', 'notes') 