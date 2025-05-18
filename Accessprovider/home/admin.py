from django.contrib import admin

# Register your models here.
from .models import (
    Fyers_Access_Token,
    Fyers_Auth_Inputs,
)

# Register your models here.


admin.site.register(Fyers_Access_Token)
admin.site.register(Fyers_Auth_Inputs)