from django.urls import path

from galleries.views import BookmarkView, PostingsView, PostingView, CommentsView, CommentView, GalleriesView, ImageView, PostingLikeView

urlpatterns = [
    path("", GalleriesView.as_view()),
    path("/<int:gallery_id>/bookmark", BookmarkView.as_view()),
    path("/bookmark-list", BookmarkView.as_view()),
    path("/<int:gallery_id>", PostingsView.as_view()),
    path("/<int:gallery_id>/<int:posting_id>", PostingView.as_view()),
    path("/<int:gallery_id>/<int:posting_id>/like", PostingLikeView.as_view()),
    path("/images", ImageView.as_view()),
    path("/<int:gallery_id>/<int:posting_id>/comments", CommentsView.as_view()),
    path("/<int:gallery_id>/<int:posting_id>/comments/<int:comment_id>", CommentView.as_view()),
]