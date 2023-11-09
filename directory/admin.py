from django.contrib import admin

from .models import SavedLocation, ServiceLocation, Regulation


@admin.register(ServiceLocation)
class ServiceLocation(admin.ModelAdmin):
    list_display = ["id",  "operator", "service", "latitude", "longitude"]
    list_filter = ["operator", "service"]
    search_fields = ["service", "description", "operator"]

@admin.register(SavedLocation)
class SavedLocationAdmin(admin.ModelAdmin):
    list_display = ["id",  "saver", "locations_count"]
    search_fields = ["body"]



@admin.register(Regulation)
class RegulationLocation(admin.ModelAdmin):
    list_display = ["id",  "region", ]
    list_filter = ["region"]
    search_fields = ["body"]
