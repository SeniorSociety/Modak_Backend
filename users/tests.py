import jwt

from django.test    import TestCase, Client
from django.core.files.uploadedfile import SimpleUploadedFile

from unittest.mock  import patch, MagicMock
from users.models   import User
from my_settings    import SECRET_KEY, ALGORITHMS

class NamecardPOSTTest(TestCase):
    def setUp(self):
        user       = User.objects.create(id = 1)
        self.token = jwt.encode({"id" : user.id}, SECRET_KEY, algorithm = ALGORITHMS)

    def tearDown(self):
        User.objects.all().delete()

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
        self.assertEqual(response.json(), {"MESSAGE" : "INVALID_TOKEN"})
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
        {"data":{
            "image" : "test.jpeg",
            "name"  : "James",
            "age"   : 4,
            "description" : "TEST",
            "namecard" : "<div>namecard</div>"
            }})
        self.assertEqual(response.status_code, 200)