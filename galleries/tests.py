import jwt
import json

from django.test   import TestCase, Client

from users.models  import User
from .models       import Gallery, Posting, Comment
from my_settings   import SECRET_KEY, ALGORITHMS

class PostingListTest(TestCase):
    def setUp(self):
        gallery = Gallery.objects.create(
            name  = "test",
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
                title   = "testpost1",
                content = "testtext1",
                user    = User.objects.get(nickname = "testuser1")
            ),
            Posting(
                gallery = gallery,
                title   = "testpost2",
                content = "testtext2",
                user    = User.objects.get(nickname = "testuser1")
            ),
            Posting(
                gallery = gallery,
                title   = "testpost3",
                content = "testtext3",
                user    = User.objects.get(nickname = "testuser1")
            ),
            Posting(
                gallery = gallery,
                title   = "testpost3",
                content = "testtext3",
                user    = User.objects.get(nickname = "testuser2")
            )
        ])

        Comment.objects.bulk_create([
            Comment(
                user    = User.objects.get(nickname = "testuser2"),
                posting = Posting.objects.get(title = "testpost1")
            ),
            Comment(
                user    = User.objects.get(nickname = "testuser1"),
                posting = Posting.objects.get(title = "testpost1")
            ),
            Comment(
                user    = User.objects.get(nickname = "testuser1"),
                posting = Posting.objects.get(title = "testpost2")
            ),
            Comment(
                user    = User.objects.get(nickname = "testuser1"),
                posting = Posting.objects.get(title = "testpost2")
            ),
        ])
    def tearDown(self):
        Comment.objects.all().delete()
        Posting.objects.all().delete()
        User.objects.all().delete()
        Gallery.objects.all().delete()

    def test_posting_list_success(self):
        client     = Client()
        gallery_id = Gallery.objects.all()[0].id
        response   = client.get(f"/galleries/{gallery_id}?page=1")
        self.assertEqual(response.status_code, 200)

    def test_posting_post_success(self):
        client       = Client()
        user_id      = User.objects.all()[0].id
        access_token = jwt.encode({'id' : user_id}, SECRET_KEY, algorithm = ALGORITHMS)
        headers      = {"HTTP_Authorization": access_token}
        gallery      = Gallery.objects.all()[0]
        body         = {"title" : "1234", "content" : "4123"}

        response   = client.post(f"/galleries/{gallery.id}", json.dumps(body), content_type='application/json', **headers)
        self.assertEqual(response.status_code, 201)

class PostingTest(TestCase) :
    def setUp(self) :
        gallery = Gallery.objects.create(
            name  = "test",
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
                title   = "testpost1",
                content = "testtext1",
                user    = User.objects.get(nickname = "testuser1")
            ),
            Posting(
                gallery = gallery,
                title   = "testpost2",
                content = "testtext2",
                user    = User.objects.get(nickname = "testuser1")
            ),
            Posting(
                gallery = gallery,
                title   = "testpost3",
                content = "testtext3",
                user    = User.objects.get(nickname = "testuser1")
            ),
            Posting(
                gallery = gallery,
                title   = "testpost3",
                content = "testtext3",
                user    = User.objects.get(nickname = "testuser2")
            )
        ])

        Comment.objects.bulk_create([
            Comment(
                user    = User.objects.get(nickname = "testuser2"),
                posting = Posting.objects.get(title = "testpost1")
            ),
            Comment(
                user    = User.objects.get(nickname = "testuser1"),
                posting = Posting.objects.get(title = "testpost1")
            ),
            Comment(
                user    = User.objects.get(nickname = "testuser1"),
                posting = Posting.objects.get(title = "testpost2")
            ),
            Comment(
                user    = User.objects.get(nickname = "testuser1"),
                posting = Posting.objects.get(title = "testpost2")
            ),
        ])

    def tearDown(self) :
        Comment.objects.all().delete()
        Posting.objects.all().delete()
        User.objects.all().delete()
        Gallery.objects.all().delete()

    def test_posting_read_success(self):
        client     = Client()
        gallery_id = Gallery.objects.all()[0].id
        posting_id = Posting.objects.all()[0].id
        response   = client.get(f"/galleries/{gallery_id}/{posting_id}")
        self.assertEqual(response.status_code, 200)

    def test_posting_patch_success(self) :
        client       = Client()
        user_id      = User.objects.all()[0].id
        access_token = jwt.encode({'id' : user_id}, SECRET_KEY, algorithm = ALGORITHMS)
        headers      = {"HTTP_Authorization" : access_token}
        gallery      = Gallery.objects.all()[0]
        posting      = Posting.objects.all()[0]
        body         = {"title" : "title", "content" : "4124"}
        response     = client.patch(f"/galleries/{gallery.id}/{posting.id}", json.dumps(body),
                               content_type = 'application/json', **headers)

        self.assertEqual(response.status_code, 201)

    def test_posting_delete_success(self) :
        client       = Client()
        user_id      = User.objects.all()[0].id
        access_token = jwt.encode({'id' : user_id}, SECRET_KEY, algorithm = ALGORITHMS)
        headers      = {"HTTP_Authorization" : access_token}
        gallery      = Gallery.objects.all()[0]
        posting      = Posting.objects.all()[0]
        response     = client.delete(f"/galleries/{gallery.id}/{posting.id}", **headers)

        self.assertEqual(response.status_code, 204)

class CommentTest(TestCase) :
    def setUp(self) :
        gallery = Gallery.objects.create(
            name  = "test",
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
                title   = "testpost1",
                content = "testtext1",
                user    = User.objects.get(nickname = "testuser1")
            ),
            Posting(
                gallery = gallery,
                title   = "testpost2",
                content = "testtext2",
                user    = User.objects.get(nickname = "testuser1")
            ),
            Posting(
                gallery = gallery,
                title   = "testpost3",
                content = "testtext3",
                user    = User.objects.get(nickname = "testuser1")
            ),
            Posting(
                gallery = gallery,
                title   = "testpost3",
                content = "testtext3",
                user    = User.objects.get(nickname = "testuser2")
            )
        ])

        Comment.objects.bulk_create([
            Comment(
                user    = User.objects.get(nickname = "testuser2"),
                posting = Posting.objects.get(title = "testpost1")
            ),
            Comment(
                user    = User.objects.get(nickname = "testuser1"),
                posting = Posting.objects.get(title = "testpost1")
            ),
            Comment(
                user    = User.objects.get(nickname = "testuser1"),
                posting = Posting.objects.get(title = "testpost2")
            ),
            Comment(
                user    = User.objects.get(nickname = "testuser1"),
                posting = Posting.objects.get(title = "testpost2")
            ),
        ])

    def tearDown(self) :
        Comment.objects.all().delete()
        Posting.objects.all().delete()
        User.objects.all().delete()
        Gallery.objects.all().delete()

    def test_comment_read_success(self) :
        client     = Client()
        gallery_id = Gallery.objects.all()[0].id
        posting_id = Posting.objects.all()[0].id
        response   = client.get(f"/galleries/{gallery_id}/{posting_id}/comments")
        self.assertEqual(response.status_code, 200)

    def test_comment_post_success(self) :
        client = Client()
        user_id = User.objects.all()[0].id
        access_token = jwt.encode({'id' : user_id}, SECRET_KEY, algorithm = ALGORITHMS)
        headers = {"HTTP_Authorization" : access_token}
        gallery = Gallery.objects.all()[0]
        posting = Posting.objects.all()[0]
        body = {"content" : "4123"}
        response = client.post(f"/galleries/{gallery.id}/{posting.id}/comments", json.dumps(body),
                               content_type = 'application/json', **headers)

        self.assertEqual(response.status_code, 201)

    def test_comment_patch_success(self) :
        client       = Client()
        user_id      = User.objects.all()[0].id
        access_token = jwt.encode({'id' : user_id}, SECRET_KEY, algorithm = ALGORITHMS)
        headers      = {"HTTP_Authorization" : access_token}
        gallery      = Gallery.objects.all()[0]
        posting      = Posting.objects.all()[0]
        comment      = Comment.objects.get(posting_id = posting.id, user_id = user_id)
        body         = {"content" : "4124"}
        response     = client.patch(f"/galleries/{gallery.id}/{posting.id}/comments/{comment.id}", json.dumps(body),
                                content_type = 'application/json', **headers)

        self.assertEqual(response.status_code, 201)

    def test_comment_delete_success(self) :
        client       = Client()
        user_id      = User.objects.all()[0].id
        access_token = jwt.encode({'id' : user_id}, SECRET_KEY, algorithm = ALGORITHMS)
        headers      = {"HTTP_Authorization" : access_token}
        gallery      = Gallery.objects.all()[0]
        posting      = Posting.objects.all()[0]
        comment      = Comment.objects.get(posting_id = posting.id, user_id = user_id)
        response     = client.delete(f"/galleries/{gallery.id}/{posting.id}/comments/{comment.id}", **headers)

        self.assertEqual(response.status_code, 204)