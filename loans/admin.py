from django.contrib import admin
from django.utils.html import format_html
from .models import LoanApplication, LoanDisbursement, Repayment
from django.urls import reverse
from django.utils.safestring import mark_safe

class RepaymentInline(admin.TabularInline):
    model = Repayment
    extra = 0
    readonly_fields = ('payment_date',)
    fields = ('amount_paid', 'payment_date', 'payment_method', 'is_late', 'late_fee', 'notes')
    can_delete = False

    def has_add_permission(self, request, obj=None):
        return False

class LoanDisbursementInline(admin.StackedInline):
    model = LoanDisbursement
    extra = 0
    readonly_fields = ('disbursement_date',)
    fields = ('disbursement_amount', 'disbursement_date', 'disbursement_method', 'mobile_money_transaction_id', 'notes')
    can_delete = False

    def has_add_permission(self, request, obj=None):
        return False

@admin.register(LoanApplication)
class LoanApplicationAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_link', 'property_link', 'amount_requested', 'loan_purpose', 
                   'status', 'application_date', 'action_buttons')
    list_filter = ('status', 'loan_purpose', 'application_date')
    search_fields = ('user__username', 'user__email', 'property__location')
    readonly_fields = ('application_date', 'review_date', 'approval_date', 'disbursement_date', 'user', 'property')
    inlines = [LoanDisbursementInline, RepaymentInline]
    date_hierarchy = 'application_date'
    ordering = ('-application_date',)
    actions = ['approve_applications', 'reject_applications']

    def user_link(self, obj):
        url = reverse('admin:auth_user_change', args=[obj.user.id])
        return format_html('<a href="{}">{}</a>', url, obj.user.username)
    user_link.short_description = 'User'

    def property_link(self, obj):
        url = reverse('admin:accounts_property_change', args=[obj.property.id])
        return format_html('<a href="{}">{}</a>', url, obj.property.location)
    property_link.short_description = 'Property'

    def action_buttons(self, obj):
        if obj.status == 'pending':
            return format_html(
                '<a class="button" href="{}">Review</a>',
                reverse('admin:loans_loanapplication_change', args=[obj.id])
            )
        return '-'
    action_buttons.short_description = 'Actions'

    @admin.action(description='Approve selected applications')
    def approve_applications(self, request, queryset):
        queryset.update(status='approved')

    @admin.action(description='Reject selected applications')
    def reject_applications(self, request, queryset):
        queryset.update(status='rejected')

@admin.register(LoanDisbursement)
class LoanDisbursementAdmin(admin.ModelAdmin):
    list_display = ('id', 'loan_application_link', 'disbursement_amount', 'disbursement_date', 'disbursement_method')
    list_filter = ('disbursement_date', 'disbursement_method')
    search_fields = ('loan_application__user__username', 'loan_application__property__location', 'mobile_money_transaction_id')
    readonly_fields = ('disbursement_date', 'loan_application')
    date_hierarchy = 'disbursement_date'
    ordering = ('-disbursement_date',)

    def loan_application_link(self, obj):
        url = reverse('admin:loans_loanapplication_change', args=[obj.loan_application.id])
        return format_html('<a href="{}">Application #{}</a>', url, obj.loan_application.id)
    loan_application_link.short_description = 'Loan Application'

@admin.register(Repayment)
class RepaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'loan_application_link', 'amount_paid', 'payment_date', 'payment_method', 'is_late')
    list_filter = ('payment_date', 'payment_method', 'is_late')
    search_fields = ('loan_application__user__username', 'mobile_money_transaction_id')
    readonly_fields = ('payment_date', 'loan_application')
    date_hierarchy = 'payment_date'
    ordering = ('-payment_date',)

    def loan_application_link(self, obj):
        url = reverse('admin:loans_loanapplication_change', args=[obj.loan_application.id])
        return format_html('<a href="{}">Application #{}</a>', url, obj.loan_application.id)
    loan_application_link.short_description = 'Loan Application'

    def has_add_permission(self, request):
        return False
