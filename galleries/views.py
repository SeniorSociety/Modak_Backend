import json

from django.core.paginator import Paginator
from django.views          import View
from django.http           import JsonResponse

from galleries.models   import Gallery, Bookmark, Posting, Comment
from users.utils        import login_decorator

class BookmarkView(View):
    @login_decorator
    def post(self, request, gallery_id):
        if not Gallery.objects.filter(id=gallery_id).exists():
            return JsonResponse({'MESSAGE' : 'GALLERY_DOES_NOT_EXIST'}, status=400)

        bookmark, is_bookmark = Bookmark.objects.get_or_create(
            gallery = Gallery.objects.get(id=gallery_id),
            user    = request.user
        )

        if not is_bookmark:
            bookmark.delete()
            return JsonResponse({'MESSAGE' : 'BOOKMARK_DELETED'}, status=204)

        return JsonResponse({'MESSAGE' : 'BOOKMARK_CREATED'}, status=201)

    @login_decorator
    def get(self, request):
        bookmarks = Bookmark.objects.select_related('gallery').filter(user_id=request.user.id)

        gallery_list = [{
            'gallery_name' : bookmark.gallery.name,
            'gallery_image' : bookmark.gallery.image
        } for bookmark in bookmarks ]

        return JsonResponse({'LIST' : gallery_list}, status=200)

class PostingsView(View):
    def get(self, request, gallery_id):
        if not Gallery.objects.filter(id=gallery_id).exists():
            return JsonResponse({"MESSAGE": "KEY_ERROR"}, status = 400)

        postingslist = Posting.objects.filter(gallery=gallery_id).select_related("user")\
            .prefetch_related("comment_set").order_by("created_at")

        pagenator = Paginator(postingslist, 10)
        page      = request.GET.get("page", 1)
        postings  = pagenator.get_page(page)
        is_next   = postings.has_next()

        response = [{
            "id"            : posting.id,
            "title"         : posting.title,
            "thumbnail"     : posting.thumbnail,
            "view_count"    : posting.view_count,
            "created_at"    : posting.created_at,
            "updated_at"    : posting.updated_at,
            "comment_count" : posting.comment_set.count(),
            "user_nickname" : posting.user.nickname,
            "user_id"       : posting.user.id,
        } for posting in postings]

        return JsonResponse({"MESSAGE" : response, "is_next" : is_next}, status=200)

    @login_decorator
    def post(self, request, gallery_id) :
        try :
            if not Gallery.objects.filter(id = gallery_id).exists() :
                return JsonResponse({"MESSAGE" : "NO_GALLERY"}, status = 404)

            data = json.loads(request.body)
            Posting.objects.create(
                gallery_id = gallery_id,
                title      = data.get("title"),
                content    = data.get("content"),
                user       = request.user,
                thumbnail  = data.get("thumbnail")
            )

            return JsonResponse({"MESSAGE" : "SUCCESS"}, status = 201)

        except KeyError :
            return JsonResponse({"message" : "KEY_ERROR"}, status = 400)

class PostingView(View):
    def get(self, request, posting_id, gallery_id):
        if not Posting.objects.filter(id = posting_id).exists():
            return JsonResponse({"MESSAGE": "KEYERROR"}, status = 400)

        posting = Posting.objects.select_related("user").prefetch_related("comment_set").get(id = posting_id)

        posting.view_count += 1
        posting.save()

        response = {
            "id"            : posting.id,
            "title"         : posting.title,
            "thumbnail"     : posting.thumbnail,
            "view_count"    : posting.view_count,
            "created_at"    : posting.created_at,
            "updated_at"    : posting.updated_at,
            "comment_count" : posting.comment_set.count(),
            "user_name"     : posting.user.nickname,
            "user_id"       : posting.user.id
        }

        return JsonResponse({"MESSAGE" : response}, status = 200)

    @login_decorator
    def patch(self, request, posting_id, gallery_id) :
        if Posting.objects.get(id = posting_id).user != request.user :
            return JsonResponse({"MESSAGE" : "NO_PERMISSION"}, status = 403)

        try :
            data = json.loads(request.body)
            Posting.objects.filter(id = posting_id).update(
                title     = data.get("title"),
                content   = data.get("content"),
                thumbnail = data.get("thumbnail")
            )
            return JsonResponse({"MESSAGE" : "SUCCESS"}, status = 201)

        except KeyError :
            return JsonResponse({"message" : "KEY_ERROR"}, status = 400)

    @login_decorator
    def delete(self, request, posting_id, gallery_id) :
        if Posting.objects.get(id = posting_id).user != request.user :
            return JsonResponse({"MESSAGE" : "NO_PERMISSION"}, status = 403)

        try :
            Posting.objects.filter(id = posting_id).delete()
            return JsonResponse({"MESSAGE" : "SUCCESS"}, status = 204)

        except KeyError :
            return JsonResponse({"message" : "KEY_ERROR"}, status = 400)

class CommentsView(View):
    def get(self, request, posting_id, gallery_id):
        commentslist = Comment.objects.filter(posting = posting_id).select_related("user").order_by("created_at")

        pagenator  = Paginator(commentslist, 10)
        page       = request.GET.get("page", 1)
        comments   = pagenator.get_page(page)
        num_pages  = pagenator.num_pages

        response = [{
            "id"            : comment.id,
            "content"       : comment.content,
            "created_at"    : comment.created_at,
            "updated_at"    : comment.updated_at,
            "user_nickname" : comment.user.nickname,
            "user_id"       : comment.user.id
        } for comment in comments]

        return JsonResponse({"MESSAGE" : response, "page_range" : num_pages}, status = 200)

    @login_decorator
    def post(self, request, posting_id, gallery_id) :
        try :
            if not Posting.objects.filter(id = posting_id).exists() :
                return JsonResponse({"MESSAGE" : "NO_POSTING"}, status = 404)

            data = json.loads(request.body)
            Comment.objects.create(
                content = data.get("content"),
                user = request.user,
                posting_id = posting_id
            )

            return JsonResponse({"MESSAGE" : "SUCCESS"}, status = 201)

        except KeyError :
            return JsonResponse({"message" : "KEY_ERROR"}, status = 400)

class CommentView(View):
    @login_decorator
    def patch(self, request, posting_id, gallery_id, comment_id):
        if Comment.objects.get(id=comment_id).user != request.user:
            return JsonResponse({"MESSAGE" : "NO_PERMISSION"}, status = 403)

        try :
            data = json.loads(request.body)
            Comment.objects.filter(id=comment_id).update(content = data.get("content"))
            return JsonResponse({"MESSAGE" : "SUCCESS"}, status = 201)

        except KeyError :
            return JsonResponse({"message" : "KEY_ERROR"}, status = 400)

    @login_decorator
    def delete(self, request, posting_id, gallery_id, comment_id) :
        if Posting.objects.get(id = comment_id).user != request.user:
            return JsonResponse({"MESSAGE" : "NO_PERMISSION"}, status = 403)

        try :
            Comment.objects.filter(id=comment_id).delete()
            return JsonResponse({"MESSAGE" : "SUCCESS"}, status = 204)

        except KeyError :
            return JsonResponse({"message" : "KEY_ERROR"}, status = 400)
