from django.urls import path

from users.views import NamecardView

urlpatterns = [
    path("/namecard", NamecardView.as_view()),
]