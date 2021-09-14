from django.http  import JsonResponse
from django.views import View

from core.utils     import CloudStorage
from users.utils    import login_decorator
from my_settings    import AWS_IAM_ACCESS_KEY_ID, AWS_S3_STORAGE_BUCKET_NAME, AWS_IAM_SECRET_ACCESS_KEY, AWS_S3_BUCKET_URL

class NamecardView(View):
    @login_decorator
    def post(self, request):
        try:
            user          = request.user
            name          = request.POST.get("name")
            age           = request.POST.get("age")
            description   = request.POST.get("description")
            namecard      = request.POST.get("namecard")
            image         = request.FILES.get("image")

            if image:
                cloud_storage = CloudStorage(id = AWS_IAM_ACCESS_KEY_ID, password = AWS_IAM_SECRET_ACCESS_KEY, bucket = AWS_S3_STORAGE_BUCKET_NAME)
                upload_key    = cloud_storage.upload_file(image)
                image         = AWS_S3_BUCKET_URL + upload_key
                
            user.name        = name if name else None
            user.age         = age if age else None
            user.description = description if description else None
            user.namecard    = namecard if namecard else None
            user.image       = image if image else None
            user.save()
            return JsonResponse({"MESSAGE":"SUCCESS"}, status=201)
        except:
            return JsonResponse({"MESSAGE":"KEY_ERROR"}, status=400)

    @login_decorator
    def get(self, request):
        user = request.user
        data = {
            "image" : user.image,
            "name"  : user.name,
            "age"   : user.age,
            "description" : user.description,
            "namecard" : user.namecard
        }
        return JsonResponse({"MESSAGE":data}, status=200)