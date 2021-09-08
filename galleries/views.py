from django.http        import JsonResponse
from django.views       import View

from galleries.models   import Gallery, Bookmark
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