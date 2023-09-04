from django.urls import path
from task.views import *

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", Logout.as_view(), name="logout"),
    path("rem/", RemoveLog.as_view(), name="rem"),
]
