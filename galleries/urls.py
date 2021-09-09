from django.urls import path

from .views import PostingsView, PostingView, CommentsView, CommentView

urlpatterns = [
    path("/<int:gallery_id>", PostingsView.as_view()),
    path("/<int:gallery_id>/<int:posting_id>", PostingView.as_view()),
    path("/<int:gallery_id>/<int:posting_id>/comments", CommentsView.as_view()),
    path("/<int:gallery_id>/<int:posting_id>/comments/<int:comment_id>", CommentView.as_view())
]