from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from core.models import User, Company, Employee, Department, CostCenter

admin.site.register(User, UserAdmin)
admin.site.register([Company, Employee, Department, CostCenter])
