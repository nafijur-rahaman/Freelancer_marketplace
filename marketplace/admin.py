from django.contrib import admin
from .models import UserModel, JobPost
# Register your models here.


admin.site.register(UserModel)
admin.site.register(JobPost)