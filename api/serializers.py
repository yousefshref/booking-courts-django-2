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

from rest_framework import serializers
from.models import CourtImage, CourtVideo, CourtFeature, CourtTool

class CourtImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourtImage
        fields = '__all__'

class CourtVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourtVideo
        fields = '__all__'

class CourtFeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourtFeature
        fields = '__all__'

class CourtToolSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourtTool
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
