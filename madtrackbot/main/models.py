from django.db import models


class TelegramUser(models.Model):
    id = models.AutoField(primary_key=True)
    full_name = models.CharField(max_length=255)
    username = models.CharField(max_length=255, null=True, blank=True)
    telegram_id = models.BigIntegerField(unique=True)
    registered_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name


class Prescriptions(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(TelegramUser, on_delete=models.CASCADE)
    medication_name = models.CharField(max_length=255, null=False)
    dosage = models.CharField(max_length=255, null=False)
    instructions = models.TextField()
    dstart_date = models.DateField()
    end_date = models.DateField()

# Create your models here.
