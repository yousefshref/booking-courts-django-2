from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
  phone = models.CharField(max_length=100, unique=True, db_index=True)
  email = models.EmailField(max_length=254, unique=True, db_index=True)
  def __str__(self):
    return self.username

  def save(self, *args, **kwargs):
    super().save(*args, **kwargs)

class ManagerProfile(models.Model):
  user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
  is_verified = models.BooleanField(default=False)

  def __str__(self):
    return self.user.username
  
  def save(self, *args, **kwargs):
    super().save(*args, **kwargs)


class StaffProfile(models.Model):
  user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
  manager = models.ForeignKey(ManagerProfile, on_delete=models.CASCADE)

  def __str__(self):
    return self.user.username

  def save(self, *args, **kwargs):
    super().save(*args, **kwargs)


class Setting(models.Model):
  user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
  # courts settings
  booking_warning = models.CharField(null=True, blank=True, max_length=100)
  limit_of_paying_in_minuts = models.IntegerField(default=0) # if null or 0 can pay any time
  limit_of_canceling_in_minuts = models.IntegerField(default=0) # if null or 0 can cancell any time

  def __str__(self):
    return self.user.username


class UserProfile(models.Model):
  user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
  
  def __str__(self):
    return self.user.username

  def save(self, *args, **kwargs):
    super().save(*args, **kwargs)


class Income(models.Model):
  user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
  amount = models.DecimalField(max_digits=10, decimal_places=2)
  description = models.TextField()
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  def __str__(self):
    return self.user.username

  def save(self, *args, **kwargs):
    super().save(*args, **kwargs)


class Expense(models.Model):
  user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
  amount = models.DecimalField(max_digits=10, decimal_places=2)
  description = models.TextField()
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  def __str__(self):
    return self.user.username

  def save(self, *args, **kwargs):
    super().save(*args, **kwargs)



class Court(models.Model):
  user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
  name = models.CharField(max_length=255)
  address = models.CharField(max_length=255)
  location_url = models.CharField(max_length=255, null=True, blank=True)

  price_per_hour = models.DecimalField(max_digits=10, decimal_places=2)

  open_from = models.TimeField()
  open_to = models.TimeField()
  close_from = models.TimeField(null=True, blank=True)
  close_to = models.TimeField(null=True, blank=True)

  is_active = models.BooleanField(default=False)

  has_ball = models.BooleanField(default=True)

  offer_time_from = models.TimeField(null=True, blank=True)
  offer_time_to = models.TimeField(null=True, blank=True)

  event_time_from = models.TimeField(null=True, blank=True)
  event_time_to = models.TimeField(null=True, blank=True)

  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  def __str__(self):
    return self.name

  def save(self, *args, **kwargs):
    super().save(*args, **kwargs)




class Book(models.Model):
  court = models.ForeignKey(Court, on_delete=models.CASCADE)
  user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
  date = models.DateField()
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  def __str__(self):
    return self.court.name

  def save(self, *args, **kwargs):
    super().save(*args, **kwargs)

paied_with_choices = (
  ('عند الحضور', 'عند الحضور'),
  ('فودافون كاش', 'فودافون كاش'),
)

class BookTime(models.Model):
  book = models.ForeignKey(Book, on_delete=models.CASCADE)
  start_time = models.TimeField()
  end_time = models.TimeField()

  with_ball = models.BooleanField(default=False)
  event_time = models.BooleanField(default=False)
  offer_time = models.BooleanField(default=False)

  is_paied = models.BooleanField(default=False)
  paied_with = models.CharField(choices=paied_with_choices, max_length=255)

  total_price = models.DecimalField(max_digits=10, decimal_places=2)

  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  def __str__(self):
    return self.book.court.name

  def save(self, *args, **kwargs):
    super().save(*args, **kwargs)



class OverTime(models.Model):
  book = models.ForeignKey(Book, on_delete=models.CASCADE)
  start_time = models.TimeField()
  end_time = models.TimeField()
  price = models.DecimalField(max_digits=10, decimal_places=2)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  def __str__(self):
    return self.book.court.name

  def save(self, *args, **kwargs):
    super().save(*args, **kwargs)










