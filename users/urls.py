from django.urls import path

from users.views import NamecardView, KakaoLoginView, NicknameView, MyProfileView, OtherProfileView, NaverLoginView

urlpatterns = [
    path('/namecard', NamecardView.as_view()),
    path('/kakao', KakaoLoginView.as_view()),
    path('/naver', NaverLoginView.as_view()),
    path('/nickname', NicknameView.as_view()),
    path('/myprofile', MyProfileView.as_view()),
    path('/<int:user_id>/profile', OtherProfileView.as_view()),
]