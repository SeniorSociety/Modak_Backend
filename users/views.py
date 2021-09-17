import jwt, json, requests

from django.http  import JsonResponse
from django.views import View

from users.models   import User, History
from core.utils     import CloudStorage
from users.utils    import login_decorator
from my_settings    import AWS_IAM_ACCESS_KEY_ID, AWS_S3_STORAGE_BUCKET_NAME, AWS_IAM_SECRET_ACCESS_KEY, AWS_S3_BUCKET_URL, SECRET_KEY, ALGORITHMS

class NamecardView(View):
    @login_decorator
    def post(self, request):
        try:
            user      = request.user
            name      = request.POST.get("userName")
            introduce = request.POST.get("introduce")
            slogan    = request.POST.get("userSlogan")
            image     = request.FILES.get("userImage")
            email     = request.POST.get("userEmail")
            local     = request.POST.get("userLocal")
            years     = request.POST.getlist("historyYear")
            titles    = request.POST.getlist("historyTitle")
            subtitles = request.POST.getlist("historySubtitle")

            if image:
                cloud_storage = CloudStorage(id = AWS_IAM_ACCESS_KEY_ID, password = AWS_IAM_SECRET_ACCESS_KEY, bucket = AWS_S3_STORAGE_BUCKET_NAME)
                upload_key    = cloud_storage.upload_file(image)
                image         = AWS_S3_BUCKET_URL + upload_key
                
            user.name      = name if name else None
            user.introduce = introduce if introduce else None
            user.slogan    = slogan if slogan else None
            user.image     = image if image else None
            user.email     = email if email else None
            user.location  = local if local else None
            user.save()

            if years:
                for i in range(len(years)):
                    history          = History.objects.create(user=user)
                    history.year     = years[i]
                    history.title    = titles[i]
                    history.subtitle = subtitles[i]
                    history.save()

            return JsonResponse({"MESSAGE":"SUCCESS"}, status=201)
        except:
            return JsonResponse({"MESSAGE":"KEY_ERROR"}, status=400)

    @login_decorator
    def get(self, request):
        user = request.user
        data = {
            "image"    : user.image,
            "name"     : user.name,
            "slogan"   : user.slogan,
            "introduce": user.introduce,
            "email"    : user.email,
            "location" : user.location,
            "works"    : [{
                "year"    : history.year,
                "title"   : history.title,
                "subtitle": history.subtitle
                } for history in History.objects.filter(user=user)]
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
