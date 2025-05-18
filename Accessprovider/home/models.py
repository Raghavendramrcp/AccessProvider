from django.db import models

# Create your models here.
from django.contrib.auth.models import User

# Create your models here.


class Fyers_Auth_Inputs(models.Model):
    # one user may have many apps
    user_ass = models.ForeignKey(User, on_delete=models.CASCADE)
    client_id = models.CharField(max_length=50, null=True, blank=True)
    secret_id = models.CharField(max_length=50, null=True, blank=True)
    redirect_url = models.CharField(
        max_length=100,
        default="https://trade.fyers.in/api-login/redirect-uri/index.html",
    )

    def __str__(self):
        return self.client_id


class Fyers_Access_Token(models.Model):
    app_ass = models.OneToOneField(Fyers_Auth_Inputs, on_delete=models.CASCADE)
    auth_code = models.CharField(max_length=1500, null=True, blank=True)

    def __str__(self):
        return f"Access Token-{self.app_ass}"