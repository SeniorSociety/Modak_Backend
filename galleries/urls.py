from django.urls import path

from galleries.views import BookmarkView

urlpatterns = [
    path('/<int:gallery_id>/bookmark', BookmarkView.as_view()),
    path('/bookmark-list', BookmarkView.as_view())
]