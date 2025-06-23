
from django.test import TestCase
from django.contrib.auth import get_user_model
from feedback.models import Feedback

User = get_user_model()

class FeedbackAdminTest(TestCase):
    def setUp(self):
        # Create a superuser for testing
        self.admin_user = User.objects.create_superuser(
            username='user', password='user', email='admin@example.com'
        )
        # Log in as this superuser
        self.client.login(username='user', password='user')

    def test_add_feedback_via_admin(self):
        response = self.client.post('/admin/feedback/feedback/add/', {
            'user': self.admin_user.id,
            'comment': 'Great app 👍',
            'gif_url': 'https://example.com/test.gif',
            'sentiment': 'Neutre',
            'rating': 4,
        }, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "was added successfully")
        self.assertTrue(Feedback.objects.filter(comment__icontains='Great').exists())

    # def test_edit_feedback_via_admin(self):
    #     feedback = Feedback.objects.create(
    #         user=self.admin_user,
    #         comment='Initial comment',
    #         sentiment='Neutre',
    #         rating=2
    #     )

    #     response = self.client.post(f'/admin/feedback/feedback/{feedback.id}/change/', {
    #         'user': self.admin_user.id,
    #         'comment': 'Updated comment',
    #         'gif_url': '',
    #         'sentiment': 'Neutre',
    #         'rating': 5,
    #     }, follow=True)

    #     self.assertEqual(response.status_code, 200)
    #     self.assertContains(response, "was changed successfully")
    #     feedback.refresh_from_db()
    #     self.assertEqual(feedback.comment, 'Updated comment')

    # def test_delete_feedback_via_admin(self):
    #     feedback = Feedback.objects.create(
    #         user=self.admin_user,
    #         comment='Delete me',
    #         rating=1
    #     )

    #     response = self.client.post(f'/admin/feedback/feedback/{feedback.id}/delete/', {
    #         'post': 'yes'
    #     }, follow=True)

    #     self.assertEqual(response.status_code, 200)
    #     self.assertContains(response, "was deleted successfully")
    #     self.assertFalse(Feedback.objects.filter(id=feedback.id).exists())
