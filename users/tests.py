import jwt

from django.test    import TestCase, Client
from django.core.files.uploadedfile import SimpleUploadedFile

from unittest.mock    import patch, MagicMock
from users.models     import User
from my_settings      import SECRET_KEY, ALGORITHMS
from galleries.models import Gallery, Posting

class NamecardPOSTTest(TestCase):
    def setUp(self):
        user       = User.objects.create(id = 1)
        self.token = jwt.encode({"id" : user.id}, SECRET_KEY, algorithm = ALGORITHMS)

    @patch("core.utils.boto3.client")
    def test_namecard_post_success(self, mocked_requests):
        client = Client()

        class MockedResponse:
            def upload(self):
                return None

        test_image = SimpleUploadedFile(
            name         = "test.jpeg",
            content      = b"file_content",
            content_type = "image/ief"
        )

        header = {"HTTP_Authorization" : self.token}

        body = {
            "name" : "James",
            "age"  : 4,
            "description" : "TESTTEST",
            "image"   : test_image,
            "namecard" : "<div>namecard</div>"
        }

        mocked_requests.upload = MagicMock(return_value = MockedResponse())
        response               = client.post("/users/namecard", body, **header)
        self.assertEqual(response.json(), {"MESSAGE" : "SUCCESS"})
        self.assertEqual(response.status_code, 201)

    @patch("core.utils.boto3.client")
    def test_namecard_not_token_post_failed(self, mocked_requests):
        client = Client()

        class MockedResponse:
            def upload(self):
                return None

        test_image = SimpleUploadedFile(
            name         = "test.jpeg",
            content      = b"file_content",
            content_type = "image/ief"
        )

        body = {
            "name" : "James",
            "age"  : 4,
            "description" : "TESTTEST",
            "image"   : test_image,
            "namecard" : "<div>namecard</div>"
        }

        mocked_requests.upload = MagicMock(return_value = MockedResponse())
        response               = client.post("/users/namecard", body)
        self.assertEqual(response.json(), {"MESSAGE": "INVALID_TOKEN"})
        self.assertEqual(response.status_code, 400)

class NamecardGETTest(TestCase):
    def setUp(self):
        test_image = SimpleUploadedFile(
            name         = "test.jpeg",
            content      = b"file_content",
            content_type = "image/ief"
        )

        user = User.objects.create(
            id = 1,
            name = "James",
            age = 4,
            description = "TEST",
            image = test_image,
            namecard = "<div>namecard</div>"
            )
        self.token = jwt.encode({"id" : user.id}, SECRET_KEY, algorithm = ALGORITHMS)

    def tearDown(self):
        User.objects.all().delete()

    def test_namecard_get_success(self):
        client   = Client()
        header = {"HTTP_Authorization" : self.token}
        response = client.get("/users/namecard", **header)
        self.assertEqual(response.json(),
        {"MESSAGE":{
            "image" : "test.jpeg",
            "name"  : "James",
            "age"   : 4,
            "description" : "TEST",
            "namecard" : "<div>namecard</div>"
            }})
        self.assertEqual(response.status_code, 200)

class KaKaoSignInTest(TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        User.objects.all().delete()

    @patch('users.views.requests')
    def test_kakao_social_login_success(self, mocked_requests):
        client = Client()

        class MockedResponse:
            def json(self):
                return {
                    'id'           : '12387623842873291',
                    'connected_at' : '2021-08-25T09:16:53Z',
                    'properties'   : {'nickname': 'Jun'},
                    'kakao_account': {
                        'profile_nickname_needs_agreement': False,
                        'profile'                         : {'nickname': '장감자'},
                        'has_email'                       : True,
                        'email_needs_agreement'           : False,
                        'is_email_valid'                  : True,
                        'is_email_verified'               : True,
                        'email'                           : 'potato@naver.com'
                    }
                }
        mocked_requests.get = MagicMock(return_value = MockedResponse())
        headers             = {'HTTP_Authorization' : 'FAKE_TOKEN'}
        response            = client.post('/users/kakao', content_type='application/json', **headers)

        self.assertEqual(response.status_code, 200)

        token    = response.json()['TOKEN']
        user_id  = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHMS)['id']
        kakao_id = User.objects.get(id=user_id).kakao

        self.assertEqual(kakao_id, '12387623842873291')

    @patch('users.views.requests')
    def test_kakao_social_login_invalid_token(self, mocked_requests):
        client   = Client()
        response = client.post('/users/kakao', content_type='application/json')

        self.assertEqual(response.json(), {'MESSAGE' : 'INVALID_TOKEN'})
        self.assertEqual(response.status_code, 400)
        
class NicknameTest(TestCase):
    def setUp(self):
        User.objects.create(
            id    = 1,
            name  = 'Jun',
            nickname = 'HoJun',
            kakao = '10210318112998147129'
        )

        User.objects.create(
            id       = 2,
            name     = 'Min',
            nickname = 'Minch',
            kakao    = '03719836378128367'
        )

        self.token = jwt.encode({'id' : 1}, SECRET_KEY, algorithm=ALGORITHMS)

    def tearDown(self):
        User.objects.all().delete()

    def test_nickname_update_success(self):
        client = Client()

        data     = {'nickname' : 'Min'}
        headers  = {'HTTP_Authorization' : self.token}
        response = client.post('/users/nickname', content_type='application/json', data=data, **headers)

        self.assertEqual(response.json(), {'MESSAGE' : 'SUCCESS'})
        self.assertEqual(response.status_code, 200)

    def test_nickname_already_exists(self):
        client = Client()

        data     = {'nickname' : 'Minch'}
        headers  = {'HTTP_Authorization' : self.token}
        response = client.post('/users/nickname', content_type='application/json', data=data, **headers)

        self.assertEqual(response.json(), {'MESSAGE' : 'NICKNAME_ALREADY_EXISTS'})
        self.assertEqual(response.status_code, 400)

    def test_nickname_update_invalid_token(self):
        client = Client()

        data     = {'nickname' : 'Min'}
        response = client.post('/users/nickname', content_type='application/json', data=data)

        self.assertEqual(response.json(), {"MESSAGE" : "INVALID_TOKEN"})
        self.assertEqual(response.status_code, 400)

class MyPositngsTest(TestCase):
    def setUp(self):
        gallery = Gallery.objects.create(
            name = "test",
            image = "image.jpg"
        )
    
        User.objects.bulk_create([
            User(nickname = "testuser1"),
            User(nickname = "testuser2")
        ]
        )
    
        Posting.objects.bulk_create([
            Posting(
                gallery = gallery,
                title = "testpost1",
                content = "testtext1",
                user = User.objects.get(nickname = "testuser1")
            ),
            Posting(
                gallery = gallery,
                title = "testpost2",
                content = "testtext2",
                user = User.objects.get(nickname = "testuser1")
            ),
            Posting(
                gallery = gallery,
                title = "testpost3",
                content = "testtext3",
                user = User.objects.get(nickname = "testuser1")
            ),
            Posting(
                gallery = gallery,
                title = "testpost4",
                content = "testtext4",
                user = User.objects.get(nickname = "testuser2")
            )
        ])

        self.token = jwt.encode({'id' : User.objects.get(nickname = "testuser1").id}, SECRET_KEY, algorithm=ALGORITHMS)

    def tearDown(self):
        Posting.objects.all().delete()
        User.objects.all().delete()
        Gallery.objects.all().delete()
        
    def test_mypage_postings_list_success(self):
        client   = Client()
        headers  = {'HTTP_Authorization' : self.token}
        response = client.get('/users/postings', **headers)

        self.assertEqual(response.status_code, 200)
