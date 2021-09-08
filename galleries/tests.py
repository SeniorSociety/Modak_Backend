from my_settings import ALGORITHMS, SECRET_KEY
import jwt

from django.test        import TestCase, Client

from users.models       import User
from galleries.models   import Gallery, Bookmark
from my_settings        import SECRET_KEY, ALGORITHMS


class BookmarkTest(TestCase):
    @classmethod
    def setUpTestData(self):
        User.objects.create(
            id          = 1,
            nickname    = 'Jun',
            kakao       = '101',
            naver       = '102',
            image       = 'Jun.jpg',
            name        = 'HoJun Jang',
            age         = 26,
            description = 'Hello!',
            namecard    = 'abcdefg'
        )

        Gallery.objects.create(
            id    = 1,
            name  = '경제',
            image = 'abc.jpg'
        )

        Bookmark.objects.create(
            id      = 1,
            user    = User.objects.get(id=1),
            gallery = Gallery.objects.get(id=1)
        )

        self.token = jwt.encode({'id' : User.objects.get(id=1).id}, SECRET_KEY, algorithm=ALGORITHMS)

    def tearDown(self):
        Gallery.objects.all().delete()
        User.objects.all().delete()

    def test_bookmark_create_success(self):
        Bookmark.objects.all().delete()

        client = Client()
        header = {'HTTP_Authorization' : self.token}
        response = client.post('/gallery/1/bookmark', **header, content_type='application/json')

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(),
            {'MESSAGE' : 'BOOKMARK_CREATED'}
        )

    def test_bookmark_delete_success(self):
        client = Client()
        header = {'HTTP_Authorization' : self.token}
        response = client.post('/gallery/1/bookmark', **header, content_type='application/json')

        self.assertEqual(response.status_code, 204)

    def test_bookmark_list(self):
        client = Client()
        header = {'HTTP_Authorization' : self.token}
        response = client.get('/gallery/bookmark-list', **header, content_type='application/json')

        self.assertEqual(response.status_code, 200)