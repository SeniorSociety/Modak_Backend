import jwt
import json

from django.test        import TestCase, Client

from users.models       import User
from galleries.models   import Gallery, Posting, Comment, Bookmark
from my_settings        import SECRET_KEY, ALGORITHMS


class BookmarkTest(TestCase):
    @classmethod
    def setUpTestData(self):
        user = User.objects.create(
            nickname    = "Jun",
            kakao       = "101",
            naver       = "102",
            image       = "Jun.jpg",
            name        = "HoJun Jang",
            age         = 26,
            description = "Hello!",
            namecard    = "abcdefg"
        )

        Gallery.objects.create(
            name  = "경제",
            image = "abc.jpg"
        )

        Bookmark.objects.create(
            user    = User.objects.get(nickname="Jun"),
            gallery = Gallery.objects.get(name="경제")
        )

        self.token = jwt.encode({"id" : user.id}, SECRET_KEY, algorithm=ALGORITHMS)

    def tearDown(self):
        Gallery.objects.all().delete()
        User.objects.all().delete()
        Bookmark.objects.all().delete()

    def test_bookmark_create_success(self):
        Bookmark.objects.all().delete()
        
        client     = Client()
        gallery_id = Gallery.objects.get(name="경제").id
        header     = {"HTTP_Authorization" : self.token}
        response   = client.post(f"/galleries/{gallery_id}/bookmark", **header, content_type="application/json")

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(),
            {"MESSAGE" : "BOOKMARK_CREATED"}
        )

    def test_bookmark_delete_success(self):
        client   = Client()
        gallery_id = Gallery.objects.get(name = "경제").id
        header   = {"HTTP_Authorization" : self.token}
        response = client.post(f"/galleries/{gallery_id}/bookmark", **header, content_type="application/json")

        self.assertEqual(response.status_code, 204)

    def test_bookmark_list(self):
        client   = Client()
        header   = {"HTTP_Authorization" : self.token}
        response = client.get("/galleries/bookmark-list", **header, content_type="application/json")

        self.assertEqual(response.status_code, 200)

class PostingListTest(TestCase):
    @classmethod
    def setUpTestData(self):
        gallery = Gallery.objects.create(
            name  = "test",
            image = "image.jpg"
        )

        User.objects.bulk_create([
            User(
                nickname    = "Jun",
                kakao       = "101",
                naver       = "102",
                image       = "Jun.jpg",
                name        = "HoJun Jang",
                age         = 26,
                description = "Hello!",
                namecard    = "abcdefg"),
            User(
                nickname    = "Min",
                kakao       = "201",
                naver       = "202",
                image       = "Min.jpg",
                name        = "Min Choi",
                age         = 26,
                description = "Hello!!",
                namecard    = "abcdefg")
            ]
        )

        Posting.objects.bulk_create([
            Posting(
                gallery = gallery,
                title   = "testpost1",
                content = "testtext1",
                user    = User.objects.get(nickname = "Jun")
            ),
            Posting(
                gallery = gallery,
                title   = "testpost2",
                content = "testtext2",
                user    = User.objects.get(nickname = "Jun")
            ),
            Posting(
                gallery = gallery,
                title   = "testpost3",
                content = "testtext3",
                user    = User.objects.get(nickname = "Jun")
            ),
            Posting(
                gallery = gallery,
                title   = "testpost3",
                content = "testtext3",
                user    = User.objects.get(nickname = "Min")
            )
        ])

        Comment.objects.bulk_create([
            Comment(
                user    = User.objects.get(nickname = "Min"),
                posting = Posting.objects.get(title = "testpost1")
            ),
            Comment(
                user    = User.objects.get(nickname = "Jun"),
                posting = Posting.objects.get(title = "testpost1")
            ),
            Comment(
                user    = User.objects.get(nickname = "Jun"),
                posting = Posting.objects.get(title = "testpost2")
            ),
            Comment(
                user    = User.objects.get(nickname = "Jun"),
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
        gallery_id = Gallery.objects.get(name="test").id
        response   = client.get(f"/galleries/{gallery_id}?page=1")
        self.assertEqual(response.status_code, 200)

    def test_posting_post_success(self):
        client       = Client()
        user         = User.objects.get(nickname = "Jun").id
        access_token = jwt.encode({"id" : user}, SECRET_KEY, algorithm = ALGORITHMS)
        headers      = {"HTTP_Authorization": access_token}
        gallery      = Gallery.objects.all()[0]
        body         = {"title" : "1234", "content" : "4123"}

        response   = client.post(f"/galleries/{gallery.id}", json.dumps(body), content_type="application/json", **headers)
        self.assertEqual(response.status_code, 201)

class PostingTest(TestCase) :
    @classmethod
    def setUpTestData(self) :
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
        access_token = jwt.encode({"id" : user_id}, SECRET_KEY, algorithm = ALGORITHMS)
        headers      = {"HTTP_Authorization" : access_token}
        gallery      = Gallery.objects.all()[0]
        posting      = Posting.objects.all()[0]
        body         = {"title" : "title", "content" : "4124"}
        response     = client.patch(f"/galleries/{gallery.id}/{posting.id}", json.dumps(body),
                               content_type = "application/json", **headers)

        self.assertEqual(response.status_code, 201)

    def test_posting_delete_success(self) :
        client       = Client()
        user_id      = User.objects.all()[0].id
        access_token = jwt.encode({"id" : user_id}, SECRET_KEY, algorithm = ALGORITHMS)
        headers      = {"HTTP_Authorization" : access_token}
        gallery      = Gallery.objects.all()[0]
        posting      = Posting.objects.all()[0]
        response     = client.delete(f"/galleries/{gallery.id}/{posting.id}", **headers)

        self.assertEqual(response.status_code, 204)

class CommentTest(TestCase) :
    @classmethod
    def setUpTestData(self) :
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
        access_token = jwt.encode({"id" : user_id}, SECRET_KEY, algorithm = ALGORITHMS)
        headers = {"HTTP_Authorization" : access_token}
        gallery = Gallery.objects.all()[0]
        posting = Posting.objects.all()[0]
        body = {"content" : "4123"}
        response = client.post(f"/galleries/{gallery.id}/{posting.id}/comments", json.dumps(body),
                               content_type = "application/json", **headers)

        self.assertEqual(response.status_code, 201)

    def test_comment_patch_success(self) :
        client       = Client()
        user_id      = User.objects.all()[0].id
        access_token = jwt.encode({"id" : user_id}, SECRET_KEY, algorithm = ALGORITHMS)
        headers      = {"HTTP_Authorization" : access_token}
        gallery      = Gallery.objects.all()[0]
        posting      = Posting.objects.all()[0]
        comment      = Comment.objects.get(posting_id = posting.id, user_id = user_id)
        body         = {"content" : "4124"}
        response     = client.patch(f"/galleries/{gallery.id}/{posting.id}/comments/{comment.id}", json.dumps(body),
                                content_type = "application/json", **headers)

        self.assertEqual(response.status_code, 201)

    def test_comment_delete_success(self) :
        client       = Client()
        user_id      = User.objects.all()[0].id
        access_token = jwt.encode({"id" : user_id}, SECRET_KEY, algorithm = ALGORITHMS)
        headers      = {"HTTP_Authorization" : access_token}
        gallery      = Gallery.objects.all()[0]
        posting      = Posting.objects.all()[0]
        comment      = Comment.objects.get(posting_id = posting.id, user_id = user_id)
        response     = client.delete(f"/galleries/{gallery.id}/{posting.id}/comments/{comment.id}", **headers)

        self.assertEqual(response.status_code, 204)