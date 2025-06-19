from django.contrib import admin
from .models import CustomUser 
from .models import GlobalSettings
from .models import  Usermanual
from .models import  Advertisement


admin.site.register(CustomUser)
admin.site.register(Usermanual)
admin.site.register(Advertisement)
@admin.register(GlobalSettings)
class GlobalSettingsAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return not GlobalSettings.objects.exists()