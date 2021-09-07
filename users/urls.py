from django.urls import path

from users.views import NamecardView, KakaoLoginView, NicknameView

urlpatterns = [
    path('/namecard', NamecardView.as_view()),
    path('/kakao', KakaoLoginView.as_view()),
    path('/nickname', NicknameView.as_view())
]