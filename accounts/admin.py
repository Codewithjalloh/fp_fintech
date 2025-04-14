from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from .models import User, Property, PropertyDocument, UserDocument

class PropertyDocumentInline(admin.TabularInline):
    model = PropertyDocument
    extra = 1
    fields = ('document_type', 'document_file', 'uploaded_at')
    readonly_fields = ('uploaded_at',)

class UserDocumentInline(admin.TabularInline):
    model = UserDocument
    extra = 1
    fields = ('document_type', 'document_file', 'uploaded_at')
    readonly_fields = ('uploaded_at',)

class PropertyAdmin(admin.ModelAdmin):
    list_display = ('id', 'property_type', 'location', 'size', 'estimated_value', 'status', 'user', 'created_at')
    list_filter = ('property_type', 'status', 'created_at')
    search_fields = ('location', 'description', 'user__username', 'user__email')
    list_select_related = ('user',)
    inlines = [PropertyDocumentInline]
    fieldsets = (
        ('Basic Information', {
            'fields': ('user', 'property_type', 'location', 'size', 'estimated_value')
        }),
        ('Details', {
            'fields': ('description', 'status')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ('created_at', 'updated_at')

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user')

    def get_actions(self, request):
        actions = super().get_actions(request)
        if request.user.has_perm('accounts.change_property'):
            actions['mark_verified'] = (self.mark_verified, 'mark_verified', 'Mark selected properties as verified')
            actions['mark_pending'] = (self.mark_pending, 'mark_pending', 'Mark selected properties as pending')
            actions['mark_rejected'] = (self.mark_rejected, 'mark_rejected', 'Mark selected properties as rejected')
        return actions

    def mark_verified(self, request, queryset):
        queryset.update(status='verified')
    mark_verified.short_description = 'Mark selected properties as verified'

    def mark_pending(self, request, queryset):
        queryset.update(status='pending')
    mark_pending.short_description = 'Mark selected properties as pending'

    def mark_rejected(self, request, queryset):
        queryset.update(status='rejected')
    mark_rejected.short_description = 'Mark selected properties as rejected'

class UserDocumentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'document_type', 'uploaded_at', 'document_link')
    list_filter = ('document_type', 'uploaded_at')
    search_fields = ('user__username', 'user__email', 'document_type')
    readonly_fields = ('uploaded_at',)
    list_select_related = ('user',)

    def document_link(self, obj):
        if obj.document_file:
            return format_html('<a href="{}" target="_blank">View Document</a>', obj.document_file.url)
        return '-'
    document_link.short_description = 'Document'

    def get_actions(self, request):
        actions = super().get_actions(request)
        if request.user.has_perm('accounts.change_userdocument'):
            actions['mark_verified'] = (self.mark_verified, 'mark_verified', 'Mark selected documents as verified')
            actions['mark_unverified'] = (self.mark_unverified, 'mark_unverified', 'Mark selected documents as unverified')
        return actions

    def mark_verified(self, request, queryset):
        queryset.update(verified=True)
    mark_verified.short_description = 'Mark selected documents as verified'

    def mark_unverified(self, request, queryset):
        queryset.update(verified=False)
    mark_unverified.short_description = 'Mark selected documents as unverified'

class CustomUserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active', 'date_joined')
    list_filter = ('is_staff', 'is_active', 'employment_status', 'date_joined')
    search_fields = ('username', 'email', 'first_name', 'last_name', 'phone_number', 'national_id')
    inlines = [UserDocumentInline]
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {
            'fields': ('first_name', 'last_name', 'email', 'phone_number', 'national_id', 'date_of_birth', 'address')
        }),
        ('Employment Info', {
            'fields': ('employment_status', 'monthly_income')
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
            'classes': ('collapse',)
        }),
        ('Important dates', {
            'fields': ('last_login', 'date_joined'),
            'classes': ('collapse',)
        }),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'first_name', 'last_name', 'phone_number'),
        }),
    )
    readonly_fields = ('last_login', 'date_joined')

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('documents')

    def get_actions(self, request):
        actions = super().get_actions(request)
        if request.user.has_perm('accounts.change_user'):
            actions['activate_users'] = (self.activate_users, 'activate_users', 'Activate selected users')
            actions['deactivate_users'] = (self.deactivate_users, 'deactivate_users', 'Deactivate selected users')
        return actions

    def activate_users(self, request, queryset):
        queryset.update(is_active=True)
    activate_users.short_description = 'Activate selected users'

    def deactivate_users(self, request, queryset):
        queryset.update(is_active=False)
    deactivate_users.short_description = 'Deactivate selected users'

admin.site.register(User, CustomUserAdmin)
admin.site.register(Property, PropertyAdmin)
admin.site.register(UserDocument, UserDocumentAdmin)
