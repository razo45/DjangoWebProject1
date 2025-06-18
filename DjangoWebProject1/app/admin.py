from django.contrib import admin
from .models import CustomUser 
from .models import GlobalSettings


admin.site.register(CustomUser)
@admin.register(GlobalSettings)
class GlobalSettingsAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return not GlobalSettings.objects.exists()