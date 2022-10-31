from django.urls import path
from .views import TeacherAssignmentView

urlpatterns = [
    path('assignments/',TeacherAssignmentView.as_view(), name="teachers-assignments")
]
