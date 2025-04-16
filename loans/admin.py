from django.contrib import admin
from django.utils.html import format_html
from .models import LoanApplication, LoanDisbursement, Repayment

class RepaymentInline(admin.TabularInline):
    model = Repayment
    extra = 0
    fields = ('amount_paid', 'payment_date', 'payment_method', 'is_late', 'late_fee')
    readonly_fields = ('payment_date',)
    can_delete = False

class LoanDisbursementInline(admin.TabularInline):
    model = LoanDisbursement
    extra = 0
    fields = ('disbursement_amount', 'disbursement_date', 'disbursement_method', 'mobile_money_transaction_id')
    readonly_fields = ('disbursement_date',)
    can_delete = False

class LoanApplicationAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'property', 'amount_requested', 'loan_purpose', 'status', 'application_date', 'action_buttons')
    list_filter = ('status', 'loan_purpose', 'application_date')
    search_fields = ('user__username', 'property__location', 'notes')
    list_select_related = ('user', 'property')
    inlines = [LoanDisbursementInline, RepaymentInline]
    fieldsets = (
        ('Basic Information', {
            'fields': ('user', 'property', 'amount_requested', 'loan_purpose')
        }),
        ('Loan Details', {
            'fields': ('repayment_period', 'interest_rate', 'status')
        }),
        ('Dates', {
            'fields': ('application_date', 'review_date', 'approval_date', 'disbursement_date'),
            'classes': ('collapse',)
        }),
        ('Additional Information', {
            'fields': ('notes',),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ('application_date', 'review_date', 'approval_date', 'disbursement_date')
    actions = ['approve_applications', 'reject_applications']

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'property')

    def action_buttons(self, obj):
        if obj.status == 'pending':
            return format_html(
                '<a class="button" href="{}">Review</a>',
                f'/admin/loans/loanapplication/{obj.id}/change/'
            )
        return '-'
    action_buttons.short_description = 'Actions'

    @admin.action(description='Approve selected applications')
    def approve_applications(self, request, queryset):
        queryset.update(status='approved')

    @admin.action(description='Reject selected applications')
    def reject_applications(self, request, queryset):
        queryset.update(status='rejected')

class LoanDisbursementAdmin(admin.ModelAdmin):
    list_display = ('id', 'loan_application', 'disbursement_amount', 'disbursement_date', 'disbursement_method', 'transaction_id')
    list_filter = ('disbursement_date', 'disbursement_method')
    search_fields = ('loan_application__user__username', 'loan_application__property__location', 'mobile_money_transaction_id')
    list_select_related = ('loan_application',)
    fieldsets = (
        ('Basic Information', {
            'fields': ('loan_application', 'disbursement_amount', 'disbursement_date')
        }),
        ('Disbursement Details', {
            'fields': ('mobile_money_transaction_id', 'disbursement_method')
        }),
        ('Notes', {
            'fields': ('notes',)
        }),
    )
    readonly_fields = ('disbursement_date',)

    def transaction_id(self, obj):
        return obj.mobile_money_transaction_id
    transaction_id.short_description = 'Transaction ID'

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('loan_application')

class RepaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'loan_application', 'amount_paid', 'payment_date', 'payment_method', 'is_late', 'late_fee', 'transaction_id')
    list_filter = ('payment_date', 'payment_method', 'is_late')
    search_fields = ('loan_application__user__username', 'mobile_money_transaction_id')
    list_select_related = ('loan_application',)
    fieldsets = (
        ('Basic Information', {
            'fields': ('loan_application', 'amount_paid', 'payment_date')
        }),
        ('Payment Details', {
            'fields': ('mobile_money_transaction_id', 'payment_method', 'is_late', 'late_fee')
        }),
        ('Notes', {
            'fields': ('notes',)
        }),
    )
    readonly_fields = ('payment_date',)

    def transaction_id(self, obj):
        return obj.mobile_money_transaction_id
    transaction_id.short_description = 'Transaction ID'

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('loan_application')

admin.site.register(LoanApplication, LoanApplicationAdmin)
admin.site.register(LoanDisbursement, LoanDisbursementAdmin)
admin.site.register(Repayment, RepaymentAdmin)
