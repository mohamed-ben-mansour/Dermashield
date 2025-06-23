
from django.test import TestCase
from django.contrib.auth import get_user_model
from forum.models import Forum

User = get_user_model()

class ForumAdminTest(TestCase):
    def setUp(self):
        # Create superuser for testing
        self.admin_user = User.objects.create_superuser(
            username='user', password='user', email='admin@example.com'
        )
        # Log in with that superuser
        self.client.login(username='user', password='user')


    def test_add_forum_via_admin(self):
        response = self.client.post('/admin/forum/forum/add/', {
            'title': 'Test Forum',
            'desc': 'This is a test forum',
            'upvotes': 0,
            'author': self.admin_user.id,
        }, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "was added successfully")
        self.assertTrue(Forum.objects.filter(title='Test Forum').exists())

    # def test_edit_forum_via_admin(self):
    #     forum = Forum.objects.create(
    #         title='Original Title',
    #         desc='Original desc',
    #         upvotes=0,
    #         author=self.admin_user
    #     )

    #     response = self.client.post(f'/admin/forum/forum/{forum.id}/change/', {
    #         'title': 'Updated Title',
    #         'desc': 'Updated desc',
    #         'upvotes': 10,
    #         'author': self.admin_user.id,
    #     }, follow=True)

    #     self.assertEqual(response.status_code, 200)
    #     self.assertContains(response, "was changed successfully")
    #     forum.refresh_from_db()
    #     self.assertEqual(forum.title, 'Updated Title')

    # def test_delete_forum_via_admin(self):
    #     forum = Forum.objects.create(
    #         title='To delete',
    #         desc='desc',
    #         upvotes=0,
    #         author=self.admin_user
    #     )

    #     response = self.client.post(f'/admin/forum/forum/{forum.id}/delete/', {
    #         'post': 'yes'
    #     }, follow=True)

    #     self.assertEqual(response.status_code, 200)
    #     self.assertContains(response, "was deleted successfully")
    #     self.assertFalse(Forum.objects.filter(id=forum.id).exists())
