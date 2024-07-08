"""
URL configuration for travel_agency project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views

urlpatterns = [
    path('signup/',views.signup,name="signup"),
    path('login/',views.login,name="login"),
    path('logout/',views.logout,name="logout"),
    path('forgote_password/',views.forgote_password,name="forgote_password"),
    path('payments/',views.payments,name='payments'),
    path('success/',views.success,name='success'),
    path('otp/',views.otp,name="otp"),
    path('newpassword/',views.newpassword,name="newpassword"),
    path('change_password/',views.change_password,name="change_password"),
    path('profile_page/',views.profile_page,name="profile_page"),
    path('change_image/',views.change_image,name="change_image"),
    path('update_profile/',views.update_profile,name="update_profile"),
    path('slot_member/ <int:pk>',views.slot_member,name="slot_member"),
    #=====================Tourist===========================
    path('',views.home,name="index"),
    path('about/',views.about,name="about"),
    path('service/',views.service,name="service"),
    path('package/',views.package,name="package"),
    path('booking/',views.booking,name="booking"),
    path('yourbooking/',views.yourbooking,name="yourbooking"),
    path('delbooking/ <int:pk>',views.delbooking,name="delbooking"),
    path('destination/',views.destination,name="destination"),
    path('team/',views.team,name="team"),
    path('testimonial/',views.testimonial,name="testimonial"),
    path('contact/',views.contact,name="contact"), 
    #===========================Agent===========================
    path('agent_index/',views.agent_index,name="agent_index"),
    path('agent_service/',views.agent_service,name="agent_service"),
    path('agent_contact/',views.agent_contact,name="agent_contact"),
    path('add_package/',views.add_package,name="add_package"),
    path('add_images/ <int:pk>',views.add_images,name="add_images"),
    path('view_all_package/',views.view_all_package,name="view_all_package"),
    path('view_your_package/',views.view_your_package,name="view_your_package"),
    path('update_package/ <int:pk>',views.update_package,name="update_package"),
    path('delete_package/ <int:pk>',views.delete_package,name="delete_package"),
    path('package_detail/ <int:pk>',views.package_detail,name="package_detail"),
]
