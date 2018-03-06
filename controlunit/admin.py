from django.contrib import admin
from models import Food ,Water , Firstaid,Rescuetool,Machine,TransportHuman,TransportGoods,Messagebox

class MessageboxAdmin (admin.ModelAdmin):
    list_display = ('fromaddr', 'toaddr','topic','message','parameter','nack','ack')

class RescuetoolAdmin(admin.ModelAdmin):
    list_display = ('user','box')

class FoodAdmin(admin.ModelAdmin):
    list_display = ('user','packet')

class WaterAdmin(admin.ModelAdmin):
    list_display = ('user','quantity')

class FirstaidAdmin(admin.ModelAdmin):
    list_display = ('user','kit')

class TransportHumanAdmin(admin.ModelAdmin):
    list_display = ('user','capacity')

class TransportGoodsAdmin(admin.ModelAdmin):
    list_display = ('user','capacity')

class MachineAdmin(admin.ModelAdmin):
    list_display = ('user','jcb','ambulance','fireengine')
# Register your models here.
admin.site.register(Food,FoodAdmin)
admin.site.register(Water,WaterAdmin)
admin.site.register(Firstaid,FirstaidAdmin)
admin.site.register(Rescuetool,RescuetoolAdmin)
admin.site.register(Machine,MachineAdmin)
admin.site.register(TransportHuman,TransportHumanAdmin)
admin.site.register(TransportGoods,TransportGoodsAdmin)
admin.site.register(Messagebox,MessageboxAdmin)
