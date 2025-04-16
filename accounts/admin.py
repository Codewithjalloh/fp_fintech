from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Property, PropertyDocument, UserDocument
from django.utils.html import format_html
from django.urls import reverse

class PropertyDocumentInline(admin.TabularInline):
    model = PropertyDocument
    extra = 1
    fields = ['document_type', 'document_file', 'verified', 'verification_notes']
    readonly_fields = ['verified']

class UserDocumentInline(admin.TabularInline):
    model = UserDocument
    extra = 1
    fields = ['document_type', 'document_file']

class PropertyAdmin(admin.ModelAdmin):
    list_display = ['property_type', 'location', 'size', 'estimated_value', 'status', 'user']
    list_filter = ['property_type', 'status']
    search_fields = ['location', 'description']
    list_select_related = ['user']
    
    def mark_verified(self, request, queryset):
        queryset.update(status='verified')
    mark_verified.short_description = "Mark selected properties as verified"
    
    def mark_pending(self, request, queryset):
        queryset.update(status='pending')
    mark_pending.short_description = "Mark selected properties as pending"
    
    def mark_rejected(self, request, queryset):
        queryset.update(status='rejected')
    mark_rejected.short_description = "Mark selected properties as rejected"
    
    actions = [mark_verified, mark_pending, mark_rejected]

class UserDocumentAdmin(admin.ModelAdmin):
    list_display = ['user', 'document_type', 'uploaded_at']
    list_filter = ['document_type']
    search_fields = ['user__username', 'user__email']
    list_select_related = ['user']

class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active']
    list_filter = ['is_staff', 'is_active', 'employment_status']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    inlines = [UserDocumentInline, PropertyDocumentInline]
    
    def activate_users(self, request, queryset):
        queryset.update(is_active=True)
    activate_users.short_description = "Activate selected users"
    
    def deactivate_users(self, request, queryset):
        queryset.update(is_active=False)
    deactivate_users.short_description = "Deactivate selected users"
    
    actions = [activate_users, deactivate_users]
    
    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('documents', 'property_documents')

admin.site.register(User, CustomUserAdmin)
admin.site.register(Property, PropertyAdmin)
admin.site.register(UserDocument, UserDocumentAdmin)
