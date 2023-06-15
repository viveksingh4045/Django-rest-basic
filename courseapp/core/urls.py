
from django.contrib import admin
from django.urls import path
from core.views import CourseList, CourseDetail

urlpatterns = [
    path("course", CourseList.as_view()),
    path("course/<int:pk>", CourseDetail.as_view()),
]
