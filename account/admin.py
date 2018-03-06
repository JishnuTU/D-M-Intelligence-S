from django.contrib import admin

from .models import Volunteer,Accomadation,Hospital,Pronearea

class VolunteerAdmin(admin.ModelAdmin):
    list_display = ('user','humanaid','status','loyalto')

class AccomadationAdmin(admin.ModelAdmin):
    list_display = ('user','capacity','status','loyalto')

class HosiptalAdmin(admin.ModelAdmin):
    list_display = ('user','canoccupy','status','loyalto')

class ProneareaAdmin(admin.ModelAdmin):
    list_display = ('user','population','status','loyalto')


admin.site.register(Volunteer,VolunteerAdmin)
admin.site.register(Accomadation,AccomadationAdmin)
admin.site.register(Hospital,HosiptalAdmin)
admin.site.register(Pronearea,ProneareaAdmin)
