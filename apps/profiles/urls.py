from django.urls import path

from apps.profiles.views import ProfileView

"""
    '' - url профайла
"""
urlpatterns = [
    path('', ProfileView.as_view())
]
