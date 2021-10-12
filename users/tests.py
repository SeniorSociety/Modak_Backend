import jwt

from django.test    import TestCase, Client
from django.core.files.uploadedfile import SimpleUploadedFile

from unittest.mock    import patch, MagicMock
from users.models     import History, User
from my_settings      import SECRET_KEY, ALGORITHMS
from galleries.models import Gallery, Posting, Bookmark

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
            "name"     : "James",
            "slogan"   : "slogan",
            "introduce": "introduce",
            "image"    : test_image,
            "local"    : "local",
            "email"    : "email",
            "titles"   : "title",
            "subtitles": "subtitle",
            "years"    : 2021
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
            "name"     : "James",
            "slogan"   : "slogan",
            "introduce": "introduce",
            "image"    : test_image,
            "local"    : "local",
            "email"    : "email",
            "titles"   : "title",
            "subtitles": "subtitle",
            "years"    : 2021
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
            id        = 1,
            name      = "James",
            slogan    = "slogan",
            introduce = "introduce",
            image     = test_image,
            email     = "email",
            location  = "location",
            )
        History.objects.create(
            id       = 1,
            year     = 1,
            title    = "title",
            subtitle = "subtitle",
            user     = user)
        self.token = jwt.encode({"id" : user.id}, SECRET_KEY, algorithm = ALGORITHMS)

    def tearDown(self):
        User.objects.all().delete()

    def test_namecard_get_success(self):
        client   = Client()
        header = {"HTTP_Authorization" : self.token}
        response = client.get("/users/namecard", **header)
        self.assertEqual(response.json(),
        {"MESSAGE":{
            "image"    : "test.jpeg",
            "name"     : "James",
            "slogan"   : "slogan",
            "introduce": "introduce",
            "email"    : "email",
            "location" : "location",
            "works"    : [{
                "year"    : 1,
                "title"   : "title",
                "subtitle": "subtitle"
                }]}})
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

class MyProfileTest(TestCase):
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
        response = client.get('/users/myprofile', **headers)

        self.assertEqual(response.status_code, 200)

class ProfileGETTest(TestCase):
    def setUp(self):
        gallery = Gallery.objects.create(
            name  = "test",
            image = "image.jpg"
        )
        test_image = SimpleUploadedFile(
            name         = "test.jpeg",
            content      = b"file_content",
            content_type = "image/ief"
        )
        User.objects.bulk_create([
            User(
                id        = 1,
                name      = "James",
                slogan    = "slogan",
                introduce = "introduce",
                image     = test_image,
                email     = "email",
                location  = "location"),
            User(
                id        = 2,
                name      = "TEST",
                slogan    = "TEST",
                introduce = "TEST",
                image     = test_image,
                email     = "TEST",
                location  = "TEST")
        ])
        profile_user = User.objects.get(id=2)
        History.objects.create(
            id       = 1,
            year     = 1,
            title    = "TEST",
            subtitle = "TEST",
            user     = profile_user)
        Posting.objects.bulk_create([
            Posting(
                gallery = gallery,
                id      = 1,
                title   = "testpost1",
                content = "testtext1",
                user    = profile_user
            ),
            Posting(
                gallery = gallery,
                id      = 2,
                title   = "testpost2",
                content = "testtext2",
                user    = profile_user
            ),
            Posting(
                gallery = gallery,
                id      = 3,
                title   = "testpost3",
                content = "testtext3",
                user    = profile_user
            ),
            Posting(
                gallery = gallery,
                id      = 4,
                title   = "testpost4",
                content = "testtext4",
                user    = profile_user
            )
        ])
        Bookmark.objects.create(
            gallery = gallery,
            user    = profile_user
        )
        user = User.objects.get(id=1)
        self.token = jwt.encode({"id" : user.id}, SECRET_KEY, algorithm = ALGORITHMS)

    def tearDown(self):
        Bookmark.objects.all().delete()
        Posting.objects.all().delete()
        History.objects.all().delete()
        User.objects.all().delete()
        Gallery.objects.all().delete()

    def test_own_profile_get_success(self):
        client   = Client()
        header = {"HTTP_Authorization" : self.token}
        response = client.get("/users/1/profile", **header)
        self.assertEqual(response.json()["MESSAGE"]["is_editable"], True)
        self.assertEqual(response.status_code, 200)

    def test_others_profile_get_success(self):
        client   = Client()
        header = {"HTTP_Authorization" : self.token}
        response = client.get("/users/2/profile", **header)
        self.assertEqual(response.json()["MESSAGE"]["is_editable"], False)
        self.assertEqual(response.status_code, 200)
    
    def test_profile_get_failed_NOT_FOUND_USER(self):
        client   = Client()
        header = {"HTTP_Authorization" : self.token}
        response = client.get("/users/100/profile", **header)
        self.assertEqual(response.json(), {'MESSAGE' : 'NOT_FOUND_USER'})
        self.assertEqual(response.status_code, 400)
