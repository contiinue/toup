from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class Vacancy(models.Model):
    user = models.ForeignKey("user.User", on_delete=models.PROTECT)
    company_name = models.CharField(max_length=128)
    name = models.CharField(max_length=127)
    experience = models.CharField(max_length=63)
    city = models.CharField(max_length=63, null=True)
    alternate_url = models.CharField(max_length=63)
    schedule = models.CharField(max_length=63)
    contact_email = models.EmailField(null=True)
    contacts_phones = PhoneNumberField(null=True)
    is_request = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Notification(models.Model):
    user = models.ForeignKey("user.User", on_delete=models.PROTECT)
    date_create = models.DateTimeField(auto_now=True)
    request_notification = models.BooleanField(default=False)
    vacancies = models.ManyToManyField(Vacancy)
