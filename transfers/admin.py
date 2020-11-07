from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from import_export.admin import ImportExportModelAdmin

from .models import *


class UserProfileInline(admin.StackedInline):
	model = UserProfile
	can_delete = False
	verbose_name_plural = 'UserProfile'
	fk_name = 'user'


class CustomUserAdmin(UserAdmin):
	inlines = (UserProfileInline,)

	def get_inline_instances(self, request, obj=None):
		if not obj:
			return []
		return super(CustomUserAdmin, self).get_inline_instances(request, obj)

class PS2TSTransferadmin(ImportExportModelAdmin):
    	list_display = ('applicant','supervisor_email','hod_email','application_date')
    	search_fields = ('applicant__user__username','supervisor_email','hod_email',)

class TS2PSTransferadmin(ImportExportModelAdmin):
    	list_display = ('applicant','hod_email','application_date')
    	search_fields = ('applicant__user__username','hod_email',)
	


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
admin.site.register(PS2TSTransfer,PS2TSTransferadmin)
admin.site.register(TS2PSTransfer,TS2PSTransferadmin)
admin.site.register(DeadlineModel)
