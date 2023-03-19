from django.contrib import admin
from .models import TelegramUser, Prescriptions


class MedTrackAdminUser(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'username', 'telegram_id', 'registered_time')


class MedTrackPrescriptions(admin.ModelAdmin):
    list_display = ('id', 'user', 'medication_name', 'dosage', 'instructions', 'dstart_date', 'end_date')


admin.site.register(TelegramUser, MedTrackAdminUser)
admin.site.register(Prescriptions, MedTrackPrescriptions)

# Register your models here.
