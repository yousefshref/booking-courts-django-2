from django.contrib import admin
from .models import CustomUser, Court, Book, BookTime, OverTime, Income, Expense, UserProfile, StaffProfile, ManagerProfile, Setting, CourtFeature, CourtImage, CourtTool, CourtVideo



admin.site.register([CustomUser, Court, Book, BookTime, OverTime, Income, Expense, UserProfile, StaffProfile, ManagerProfile, Setting, CourtFeature, CourtImage, CourtTool, CourtVideo])
