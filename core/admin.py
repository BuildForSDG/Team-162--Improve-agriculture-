"""
Core admin setup
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from core.forms import CustomUserCreationForm
from core.models import User


@admin.register(User)
class UserCoreAdmin(UserAdmin):
	fieldsets = (
		(_('Credentials'), {'fields': ('username', 'password')}),
		(_('Personal info'), {
			'fields': ('first_name', 'last_name', 'other_name', 'email', 'phone_number', 'gender')}),
		(_('Others'), {'fields': ('bio', 'profile_image_url', 'account_type', 'status')}),
		(_('Permissions'), {
			'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
		}),
		(_('Important dates'), {'fields': ('last_login', 'date_joined')}),
	)

	list_filter = ('date_created', 'gender', 'account_type', 'status')
	date_hierarchy = 'date_created'
	list_display = (
		'username', 'full_name', 'gender', 'email', 'phone_number', 'account_type', 'status', 'date_modified',
		'date_created')
	search_fields = (
		'username', 'full_name', 'gender', 'email', 'phone_number', 'account_type__name', 'status__name')