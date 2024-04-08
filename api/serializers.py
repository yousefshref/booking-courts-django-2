from rest_framework import serializers
from . import models

class UserSerializer(serializers.ModelSerializer):
  class Meta(object):
    model = models.CustomUser
    fields = '__all__'


class ManagerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ManagerProfile
        fields = '__all__'

class StaffProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.StaffProfile
        fields = '__all__'

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserProfile
        fields = '__all__'

class IncomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Income
        fields = '__all__'

class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Expense
        fields = '__all__'

class CourtSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Court
        fields = '__all__'

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Book
        fields = '__all__'

class BookTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.BookTime
        fields = '__all__'

class OverTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.OverTime
        fields = '__all__'

class SettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Setting
        fields = '__all__'
