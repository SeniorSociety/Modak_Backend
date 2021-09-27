from django.urls import path

from users.views import NamecardView, KakaoLoginView, NicknameView, MyPostingsView

urlpatterns = [
    path('/namecard', NamecardView.as_view()),
    path('/kakao', KakaoLoginView.as_view()),
    path('/nickname', NicknameView.as_view()),
    path('/postings', MyPostingsView.as_view()),
]