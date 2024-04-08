
from django.contrib import admin
from django.urls import path, include

from api import views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('signup-verification/', views.signup_send_verification),
    path('signup/', views.signup),
    path('login/', views.login),


    path('manager/profile/', views.manager_profile),
    path('staff/profile/', views.staff_profile),
    path('user/profile/', views.user_profile),
    path('settings/', views.settings),
    path('income/', views.income),
    path('expense/', views.expense),
    path('court/', views.court),
    path('book/', views.book),
    path('book_time/', views.book_time),
    path('over_time/', views.over_time),


]
