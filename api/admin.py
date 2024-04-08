from django.contrib import admin
from .models import CustomUser, Court, Book, BookTime, OverTime, Income, Expense, UserProfile, StaffProfile, ManagerProfile

# Register your models here.


admin.site.register([CustomUser, Court, Book, BookTime, OverTime, Income, Expense, UserProfile, StaffProfile, ManagerProfile])
