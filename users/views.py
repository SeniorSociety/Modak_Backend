import jwt, json, requests

from django.http  import JsonResponse
from django.views import View

from users.models     import User
from core.utils       import CloudStorage
from users.utils      import login_decorator
from my_settings      import AWS_IAM_ACCESS_KEY_ID, AWS_S3_STORAGE_BUCKET_NAME, AWS_IAM_SECRET_ACCESS_KEY, AWS_S3_BUCKET_URL, SECRET_KEY, ALGORITHMS
from galleries.models import Posting

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

class KakaoLoginView(View):
    def post(self, request):
        try:
            access_token = request.headers.get('Authorization')

            if not access_token:
                return JsonResponse({'MESSAGE' : 'INVALID_TOKEN'}, status=400)

            response = requests.get(
                "https://kapi.kakao.com/v2/user/me",
                headers = {'Authorization': f'Bearer {access_token}'},
                timeout=3
            ).json()

            print(response)

            user, created = User.objects.get_or_create(
                kakao = response['id']
            )

            token = jwt.encode({'id' : user.id}, SECRET_KEY, algorithm = ALGORITHMS)

            return JsonResponse({
                'MESSAGE' : 'SUCCESS',
                'TOKEN' : token
            }, status=200)

        except KeyError:
            return JsonResponse({'MESSAGE' : 'KEY_ERROR'}, status=400)

class NicknameView(View):
    @login_decorator
    def post(self, request):
        try:
            nickname = json.loads(request.body)['nickname']
            user = request.user

            if User.objects.filter(nickname=nickname).exists():
                return JsonResponse({'MESSAGE' : 'NICKNAME_ALREADY_EXISTS'}, status=400)
            
            user.nickname = nickname
            user.save()
            
            return JsonResponse({'MESSAGE' : 'SUCCESS'}, status=200)

        except KeyError:
            return JsonResponse({'MESSAGE' : 'KEY_ERROR'}, status=400)

class MyPostingsView(View):
    @login_decorator
    def get(self, request):
        postings = Posting.objects.filter(user=request.user).select_related("gallery")
        
        posts = [{
            "gallery_id" : posting.gallery.id,
            "id"         : posting.id,
            "title"      : posting.title,
            "content"    : posting.content,
            "created_at" : posting.created_at
        } for posting in postings]
        
        return JsonResponse({'MESSAGE' : posts}, status = 200)