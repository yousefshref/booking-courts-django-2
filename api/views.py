from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from django.shortcuts import get_object_or_404
from rest_framework.authtoken.models import Token

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from django.db.models import Q
import random

from django.core.cache import cache
from datetime import datetime, timedelta

from . import serializers
from . import models

def send_email(receiver_email, subject, message_body):
  # Email configuration
  sender_email = 'yb2005at@gmail.com'
  sender_password = 'ixvn wnfs airn gcqs'

  # Create message container
  msg = MIMEMultipart()
  msg['From'] = sender_email
  msg['To'] = receiver_email
  msg['Subject'] = subject

  # Attach message body
  msg.attach(MIMEText(message_body, 'plain'))

  # Connect to SMTP server
  smtp_server = smtplib.SMTP('smtp.gmail.com', 587)  # Change to your SMTP server and port
  smtp_server.starttls()  # Enable TLS encryption

  # Login to the SMTP server
  smtp_server.login(sender_email, sender_password)

  # Send email
  smtp_server.sendmail(sender_email, receiver_email, msg.as_string())

  # Close connection to SMTP server
  smtp_server.quit()

  return True


@api_view(['POST'])
def signup_send_verification(request):
  data = request.data.copy()
  serializer = serializers.UserSerializer(data=request.data)
  if serializer.is_valid():
    random_numbers = random.randint(100000, 999999)
    send_email(request.data['email'], "تأكيد حسابك", f"كود تفعيل حسابك {random_numbers} لا تشاركة مع احد")
    data['verification'] = random_numbers
    cache.set('verification', data, timeout=3600)
  return Response(serializer.errors, status=status.HTTP_200_OK)


@api_view(['POST'])
def signup(request):
  data = request.data.copy()
  serializer = serializers.UserSerializer(data=data)
  if serializer.is_valid():
    cach_data = cache.get('verification')
    
    serializer.save() 

    if(str(data['phone']) == str(cach_data['phone']) and str(data['verification']) == str(cach_data['verification'])):
      user = models.CustomUser.objects.get(phone=request.data['phone'])
      user.set_password(request.data['password'])
      user.save()

      token = Token.objects.create(user=user)
      return Response({'token': token.key, 'user': serializer.data})
    else:
      return Response({'error': "البيانات خاطئة"})

  return Response(serializer.errors, status=status.HTTP_200_OK)


@api_view(['POST'])
def login(request):
  user = get_object_or_404(models.CustomUser, phone=request.data['phone'])
  if not user.check_password(request.data['password']):
    return Response("missing user", status=status.HTTP_404_NOT_FOUND)
  token, created = Token.objects.get_or_create(user=user)

  if not models.UserProfile.objects.filter(user=user).exists():
    profile = models.UserProfile(user=user)
    profile.save()

  serializer = serializers.UserSerializer(user)
  return Response({'token': token.key, 'user': serializer.data})



@api_view(['GET', 'POST', 'PUT'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def manager_profile(request):
  if request.method == 'GET':
    manager = models.ManagerProfile.objects.get(user=request.user)
    serializer = serializers.ManagerProfileSerializer(manager)
    return Response(serializer.data)

  if request.method == 'POST':
    try:
      manager = models.ManagerProfile.objects.get(user=request.user)
      return Response({"error": "manager already exists"})
    except models.ManagerProfile.DoesNotExist:
      serializer = serializers.ManagerProfileSerializer(data=request.data)
      if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  
  if request.method == 'PUT':
    manager = models.ManagerProfile.objects.get(user=request.user)
    serializer = serializers.ManagerProfileSerializer(manager, data=request.data, partial=True)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




@api_view(['GET', 'POST', 'PUT'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def staff_profile(request):
  if request.method == 'GET':
    staff = models.StaffProfile.objects.get(user=request.user)
    serializer = serializers.StaffProfileSerializer(staff)
    return Response(serializer.data)

  if request.method == 'POST':
    try:
      staff = models.StaffProfile.objects.get(user=request.user)
      return Response({"error": "staff already exists"})
    except models.StaffProfile.DoesNotExist:
      serializer = serializers.StaffProfileSerializer(data=request.data)
      if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  
  if request.method == 'PUT':
    staff = models.StaffProfile.objects.get(user=request.user)
    serializer = serializers.StaffProfileSerializer(staff, data=request.data, partial=True)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




@api_view(['GET', 'POST', 'PUT'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def user_profile(request):
  if request.method == 'GET':
    user = models.UserProfile.objects.get(user=request.user)
    serializer = serializers.UserProfileSerializer(user)
    return Response(serializer.data)

  if request.method == 'POST':
    try:
      user = models.UserProfile.objects.get(user=request.user)
      return Response({"error": "user already exists"})
    except:
      serializer = serializers.UserProfileSerializer(data=request.data)
      if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  
  if request.method == 'PUT':
    user = models.UserProfile.objects.get(user=request.user)
    serializer = serializers.UserProfileSerializer(user, data=request.data, partial=True)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def income(request):
  if request.method == 'GET':
    income = models.Income.objects.filter(user=request.user)
    serializer = serializers.IncomeSerializer(income, many=True)
    return Response(serializer.data)

  if request.method == 'POST':
    serializer = serializers.IncomeSerializer(data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  
  if request.method == 'PUT':
    income = models.Income.objects.get(user=request.user, id=request.data['id'])
    serializer = serializers.IncomeSerializer(income, data=request.data, partial=True)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  
  if request.method == 'DELETE':
    income = models.Income.objects.get(user=request.user, id=request.data['id'])
    income.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)




@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def expense(request):
  if request.method == 'GET':
    expense = models.Expense.objects.filter(user=request.user)
    serializer = serializers.ExpenseSerializer(expense, many=True)
    return Response(serializer.data)

  if request.method == 'POST':
    serializer = serializers.ExpenseSerializer(data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  
  if request.method == 'PUT':
    expense = models.Expense.objects.get(user=request.user, id=request.data['id'])
    serializer = serializers.ExpenseSerializer(expense, data=request.data, partial=True)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  
  if request.method == 'DELETE':
    expense = models.Expense.objects.get(user=request.user, id=request.data['id'])
    expense.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)




@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def court(request):
  if request.method == 'GET':
    court = models.Court.objects.all()

    if request.GET.get('id'):
      court = models.Court.objects.get(id=request.GET.get('id'))
      serializer = serializers.CourtSerializer(court)
      return Response(serializer.data)

    manager_profile = models.ManagerProfile.objects.get(user=request.user)
    staff_profile = models.StaffProfile.objects.get(user=request.user)

    if manager_profile:
      staffs = models.StaffProfile.objects.filter(manager=manager_profile)
      ids = [staff.user.id for staff in staffs]
      court = court.filter(user__id__in=ids)

    if staff_profile:
      manager = models.ManagerProfile.objects.get(user=staff_profile.manager.user.pk)
      staffs = models.StaffProfile.objects.filter(manager=manager)
      ids = [staff.user.id for staff in staffs]
      court = court.filter(user__id__in=ids)



    serializer = serializers.CourtSerializer(court, many=True)
    return Response(serializer.data)

  if request.method == 'POST':
    serializer = serializers.CourtSerializer(data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  
  if request.method == 'PUT':
    court = models.Court.objects.get(id=request.data['id'])
    serializer = serializers.CourtSerializer(court, data=request.data, partial=True)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  
  if request.method == 'DELETE':
    court = models.Court.objects.get(id=request.data['id'])
    court.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)



@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def book(request):
  if request.method == 'GET':
    book = models.Book.objects.all()

    if request.GET.get('id'):
      book = models.Book.objects.get(id=request.GET.get('id'))
      serializer = serializers.BookSerializer(book)
      return Response(serializer.data)

    manager_profile = models.ManagerProfile.objects.get(user=request.user)
    staff_profile = models.StaffProfile.objects.get(user=request.user)
    user_profile = models.UserProfile.objects.get(user=request.user)

    if manager_profile:
      staffs = models.StaffProfile.objects.filter(manager=manager_profile)
      ids = [staff.user.id for staff in staffs]
      book = book.filter(court__user__id__in=ids)

    if staff_profile:
      manager = models.ManagerProfile.objects.get(user=staff_profile.manager.user.pk)
      staffs = models.StaffProfile.objects.filter(manager=manager)
      ids = [staff.user.id for staff in staffs]
      book = book.filter(court__user__id__in=ids)

    if user_profile:
      book = models.Court.objects.filter(user=user_profile.user)

    serializer = serializers.BookSerializer(book, many=True)
    return Response(serializer.data)
  
  if request.method == 'POST':
    data = request.data.copy()
    data['user'] = request.user.id
    serializer = serializers.BookSerializer(data=data)
    if serializer.is_valid():
      send_email(request.user.email, "عملية حجز ناجحة: ", "تم حجز الملعب بنجاح")
      serializer.save()
      return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  
  if request.method == 'PUT':
    book = models.Book.objects.get(id=request.data['id'])
    serializer = serializers.BookSerializer(book, data=request.data, partial=True)
    if serializer.is_valid():
      send_email(request.user.email, "تعديل علي الحجز: ", "تم تغيير بعض بيانات الحجز")
      serializer.save()
      return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  if request.method == 'DELETE':
    book = models.Book.objects.get(id=request.data['id'])
    book.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
  


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def book_time(request):
  if request.method == 'GET':
    book_time = models.BookTime.objects.all()

    manager_profile = models.ManagerProfile.objects.get(user=request.user)
    staff_profile = models.StaffProfile.objects.get(user=request.user)
    user_profile = models.UserProfile.objects.get(user=request.user)

    if manager_profile:
      staffs = models.StaffProfile.objects.filter(manager=manager_profile)
      ids = [staff.user.id for staff in staffs]
      book_time = book_time.filter(book__user__id__in=ids)

    if staff_profile:
      manager = models.ManagerProfile.objects.get(user=staff_profile.manager.user.pk)
      staffs = models.StaffProfile.objects.filter(manager=manager)
      ids = [staff.user.id for staff in staffs]
      book_time = book_time.filter(book__user__id__in=ids)

    if user_profile:
      book_time = models.BookTime.objects.filter(book__user=user_profile.user)

    serializer = serializers.BookTimeSerializer(book_time, many=True)
    return Response(serializer.data)

  if request.method == 'POST':
    serializer = serializers.BookTimeSerializer(data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  
  if request.method == 'PUT':
    book_time = models.BookTime.objects.get(id=request.data['id'])
    serializer = serializers.BookTimeSerializer(book_time, data=request.data, partial=True)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  
  if request.method == 'DELETE':
    book_time = models.BookTime.objects.get(id=request.data['id'])
    book_time.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)




@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def over_time(request):
  if request.method == 'GET':
    over_time = models.OverTime.objects.filter(book=request.GET.get('book_id'))

    if request.GET.get('id'):
      over_time = models.OverTime.objects.get(id=request.GET.get('id'))
      serializer = serializers.OverTimeSerializer(over_time)
      return Response(serializer.data)

    serializer = serializers.OverTimeSerializer(over_time, many=True)
    return Response(serializer.data)

  if request.method == 'POST':
    serializer = serializers.OverTimeSerializer(data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  
  if request.method == 'PUT':
    over_time = models.OverTime.objects.get(id=request.data['id'])
    serializer = serializers.OverTimeSerializer(over_time, data=request.data, partial=True)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  
  if request.method == 'DELETE':
    over_time = models.OverTime.objects.get(id=request.data['id'])
    over_time.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)



@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def settings(request, pk):
  if request.method == 'GET':
    settings = models.Settings.objects.get(id=pk)
    serializer = serializers.SettingsSerializer(settings)
    return Response(serializer.data)
  
  if request.method == 'PUT':
    settings = models.Settings.objects.get(id=pk)
    serializer = serializers.SettingsSerializer(settings, data=request.data, partial=True)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    




def time_slots_between(start_time_str, end_time_str):
    # Convert input strings to datetime objects
    start_time = datetime.strptime(start_time_str, "%H:%M")
    end_time = datetime.strptime(end_time_str, "%H:%M")

    if start_time == end_time:
        # Return a 24-hour cycle starting from the given time
        time_slots = []
        current_time = start_time
        for _ in range(48):  # 24 hours * 2 slots per hour
            time_slots.append(current_time.strftime("%H:%M"))
            current_time += timedelta(minutes=30)  # Increment by 30 minutes
        return time_slots

    # Initialize list to hold time slots
    time_slots = []

    # Increment time in slots and append to list until end time is reached
    current_time = start_time
    while current_time <= end_time:
        time_slots.append(current_time.strftime("%H:%M"))
        current_time += timedelta(minutes=60)  # Increment by 30 minutes

    return time_slots

@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def check_court_before_book(request, court_id):
  court = models.Court.objects.get(id=court_id)

  date = datetime.strptime(request.GET.get('date'), "%Y-%m-%d").strftime("%Y-%m-%d")

  open_from = court.open_from.strftime("%H:%M")
  open_to = court.open_to.strftime("%H:%M")
  
  close_from = None
  close_to = None
  closed_times = []

  if court.close_from is not None and court.close_to is not None:
    close_from = court.open_from.strftime("%H:%M")
    close_to = court.open_to.strftime("%H:%M")
    closed_times = time_slots_between(close_from, close_to)

  times = time_slots_between(open_from, open_to)
  booked_times_arr = []
  booked_times = models.BookTime.objects.filter(court=court_id, book__date=date)
  for i in booked_times:
    booked_times_arr.append(i.start_time.strftime("%H:%M"), i.end_time.strftime("%H:%M"))


  data = {
    "times": times,
    "booked_times": booked_times_arr,
    "closed_times": closed_times
  }

  return Response(data)








