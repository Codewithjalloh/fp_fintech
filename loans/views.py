from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import LoanApplicationForm, LoanDisbursementForm, RepaymentForm
from .models import LoanApplication, LoanDisbursement, Repayment

# Create your views here.

def test_template(request):
    return render(request, 'loans/test.html')

@login_required
def loan_application(request):
    if request.method == 'POST':
        form = LoanApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            loan_application = form.save(commit=False)
            loan_application.user = request.user
            loan_application.save()
            messages.success(request, 'Loan application submitted successfully!')
            return redirect('loans:applications')
    else:
        form = LoanApplicationForm()
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
