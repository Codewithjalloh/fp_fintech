from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Field
from .models import LoanApplication, LoanDisbursement, Repayment

class LoanApplicationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        # Filter properties to only show user's properties
        if self.user:
            self.fields['property'].queryset = self.user.properties.all()
        
        # Set up crispy forms
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('property', css_class='form-group col-md-6 mb-0'),
                Column('amount_requested', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('loan_purpose', css_class='form-group col-md-6 mb-0'),
                Column('repayment_period', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            'notes',
            Submit('submit', 'Submit Application', css_class='btn btn-primary w-100 mt-3')
        )
        
        # Add placeholders and help text
        self.fields['property'].widget.attrs.update({'class': 'form-select'})
        self.fields['amount_requested'].widget.attrs.update({
            'placeholder': 'Enter loan amount',
            'min': '0',
            'step': '0.01'
        })
        self.fields['loan_purpose'].widget.attrs.update({'class': 'form-select'})
        self.fields['repayment_period'].widget.attrs.update({
            'placeholder': 'Enter repayment period in months',
            'min': '1',
            'max': '60'
        })
        self.fields['notes'].widget.attrs.update({
            'placeholder': 'Provide any additional information',
            'rows': 4
        })
        
        # Set field labels
        self.fields['property'].label = 'Select Property'
        self.fields['amount_requested'].label = 'Loan Amount'
        self.fields['loan_purpose'].label = 'Loan Purpose'
        self.fields['repayment_period'].label = 'Repayment Period'
        self.fields['notes'].label = 'Additional Notes'
        
        # Set help text
        self.fields['property'].help_text = 'Choose the property you want to use as collateral'
        self.fields['amount_requested'].help_text = 'Enter the amount you wish to borrow'
        self.fields['loan_purpose'].help_text = 'Select the primary purpose for this loan'
        self.fields['repayment_period'].help_text = 'Choose your preferred repayment duration in months'
        self.fields['notes'].help_text = 'Provide any additional information that might help with your loan application'

    class Meta:
        model = LoanApplication
        fields = ('property', 'loan_purpose', 'amount_requested', 'repayment_period', 'notes')
        widgets = {
            'amount_requested': forms.NumberInput(attrs={'class': 'form-control'}),
            'repayment_period': forms.NumberInput(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control'}),
        }

class LoanDisbursementForm(forms.ModelForm):
    class Meta:
        model = LoanDisbursement
        fields = ('loan_application', 'disbursement_amount', 'disbursement_method', 'mobile_money_transaction_id', 'notes')

class RepaymentForm(forms.ModelForm):
    class Meta:
        model = Repayment
        fields = ('loan_application', 'amount_paid', 'payment_method', 'mobile_money_transaction_id', 'notes') 