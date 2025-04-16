from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import LoanApplicationForm, LoanDisbursementForm, RepaymentForm
from .models import LoanApplication, LoanDisbursement, Repayment
from accounts.models import Property

# Create your views here.

def test_template(request):
    return render(request, 'loans/test.html')

@login_required
def loan_application(request, property_id=None):
    if request.method == 'POST':
        form = LoanApplicationForm(request.POST, user=request.user)
        if form.is_valid():
            loan_application = form.save(commit=False)
            loan_application.user = request.user
            loan_application.interest_rate = 12.0  # Set default interest rate to 12%
            if property_id:
                loan_application.property = get_object_or_404(Property, id=property_id, user=request.user)
            loan_application.save()
            messages.success(request, 'Loan application submitted successfully!')
            return redirect('loans:applications')
    else:
        initial_data = {}
        if property_id:
            property = get_object_or_404(Property, id=property_id, user=request.user)
            initial_data['property'] = property
        form = LoanApplicationForm(initial=initial_data, user=request.user)
    return render(request, 'loans/apply.html', {'form': form})

@login_required
def loan_applications(request):
    applications = LoanApplication.objects.filter(user=request.user)
    return render(request, 'loans/applications.html', {'applications': applications})

@login_required
def loan_application_detail(request, pk):
    application = get_object_or_404(LoanApplication, pk=pk, user=request.user)
    return render(request, 'loans/application_detail.html', {'application': application})

@login_required
def repayments(request):
    repayments = Repayment.objects.filter(loan_disbursement__loan_application__user=request.user)
    return render(request, 'loans/repayments.html', {'repayments': repayments})

@login_required
def loan_application_edit(request, pk):
    application = get_object_or_404(LoanApplication, pk=pk, user=request.user)
    if application.status != 'pending':
        messages.error(request, 'You can only edit pending applications.')
        return redirect('loans:application_detail', pk=application.pk)
    
    if request.method == 'POST':
        form = LoanApplicationForm(request.POST, instance=application, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Loan application updated successfully!')
            return redirect('loans:application_detail', pk=application.pk)
    else:
        form = LoanApplicationForm(instance=application, user=request.user)
    
    return render(request, 'loans/apply.html', {
        'form': form,
        'application': application,
        'is_edit': True
    })

@login_required
def loan_application_cancel(request, pk):
    application = get_object_or_404(LoanApplication, pk=pk, user=request.user)
    if application.status != 'pending':
        messages.error(request, 'You can only cancel pending applications.')
        return redirect('loans:application_detail', pk=application.pk)
    
    if request.method == 'POST':
        application.status = 'cancelled'
        application.save()
        messages.success(request, 'Loan application cancelled successfully.')
        return redirect('loans:applications')
    
    return redirect('loans:application_detail', pk=application.pk)
